"""API views for the notices app"""

import html
import logging
import re

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import get_language_from_request
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView


try:
    from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
except ImportError:
    BearerAuthenticationAllowInactiveUser = None

try:
    from eventtracking import tracker
except ImportError:
    tracker = None

from notices.api import get_unacknowledged_notices_for_user
from notices.data import AcknowledgmentResponseTypes
from notices.models import AcknowledgedNotice, Notice
from notices.selectors import get_refund_policy_notice_for_user
from notices.toggles import ENABLE_NOTICES, SHOW_REFUND_POLICY_NOTICE


# Pulling this out so tests can ignore Bearer auth since we won't have platform importable in tests
COMMON_AUTH_CLASSES = [JwtAuthentication, SessionAuthentication, SessionAuthenticationAllowInactiveUser]
if BearerAuthenticationAllowInactiveUser is not None:
    COMMON_AUTH_CLASSES.append(BearerAuthenticationAllowInactiveUser)

log = logging.getLogger(__name__)

NOTICE_DISPLAYED_EVENT = "edx.bi.user.displayed_notice"
NOTICE_ACKNOWLEDGED_EVENT = "edx.bi.user.acknowledged_notice"


def _emit_tracking_event(name, data):
    """Emit a server-side tracking event. A no-op outside of edx-platform, where eventtracking is unavailable."""
    if tracker is not None:
        tracker.emit(name, data)


def _html_to_text(html_content):
    """
    Return the plain text of a notice's HTML, with paragraphs separated by one blank line.

    The result does not depend on how the HTML source is laid out in Django Admin: each line is trimmed and runs of
    blank lines are collapsed. `strip_tags` alone would run separate paragraphs together ("<p>a</p><p>b</p>" becomes
    "ab"). Links keep only their text, and the contents of `<style>`, `<script>` or `<button>` are kept as text.
    """
    text = re.sub(r"(?i)<br\s*/?>|</li>", "\n", html_content)
    text = re.sub(r"(?i)</(?:p|div|h[1-6])>", "\n\n", text)
    text = html.unescape(strip_tags(text))
    text = re.sub(r"[^\S\n]*\n[^\S\n]*", "\n", text.replace("\r\n", "\n"))  # trim each line, drop indentation
    return re.sub(r"\n{3,}", "\n\n", text).strip()


class ListUnacknowledgedNotices(APIView):
    """
    Read only view to list all notices that the user hasn't acknowledged.

    If `mobile=true` is in the query text, it will append `mobile=true` to the render links.

    Path: `/notices/api/v1/unacknowledged`

    Returns:
      * 200: OK - Contains a list of active unacknowledged notices the user still needs to see
      * 401: The requesting user is not authenticated.
      * 404: This app is not installed

    Example:
    {
        "results": [
            "http://localhost:18000/notices/render/1/",
            "http://localhost:18000/notices/render/2/",
        ]
    }
    """

    authentication_classes = COMMON_AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Return a list of all active unacknowledged notices for the user
        """
        # If feature isn't enabled for request, return empty list so the user doesn't get
        # forwarded anywhere client side
        if not ENABLE_NOTICES.is_enabled():
            return Response({"results": []}, status=HTTP_200_OK)

        in_app = request.query_params.get("mobile") == "true"

        # If request is from mobile and mobile is disabled, return empty list so user
        # doesn't get forwarded anywhere
        if in_app and not settings.NOTICES_ENABLE_MOBILE:
            return Response({"results": []}, status=HTTP_200_OK)

        unacknowledged_active_notices = get_unacknowledged_notices_for_user(
            request.user, in_app=in_app, request=request
        )

        return Response({"results": unacknowledged_active_notices}, status=HTTP_200_OK)


class RefundPolicyNotice(APIView):
    """
    Read only view returning the refund policy change notice as JSON, for display in a modal by an MFE.

    Path: `/notices/api/v1/refund-policy`

    Returns:
      * 200: OK - `show` is false when the flag is off, the notice does not exist or the user already
        acknowledged it. Otherwise it also carries the notice id and its (plain text) body.
      * 401: The requesting user is not authenticated.

    Example:
    {"show": true, "notice_id": 3, "body": "Refund rules are changing...", "language": "en"}

    The user acknowledges the notice with `POST /notices/api/v1/acknowledge` (`acknowledgment_type=confirmed`).
    """

    authentication_classes = COMMON_AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Return the refund policy notice if the user still has to acknowledge it
        """
        if not SHOW_REFUND_POLICY_NOTICE.is_enabled():
            return Response({"show": False}, status=HTTP_200_OK)

        notice = get_refund_policy_notice_for_user(request.user)
        if notice is None:
            return Response({"show": False}, status=HTTP_200_OK)

        user_language = get_language_from_request(request)
        fallback_language = settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"]
        translations = notice.translated_notice_content
        content = (
            translations.filter(language_code=user_language).first()
            or translations.filter(language_code=fallback_language).first()
        )
        if content is None:
            log.warning(f"Refund policy notice {notice.id} has no content for {user_language} or {fallback_language}")
            return Response({"show": False}, status=HTTP_200_OK)

        _emit_tracking_event(NOTICE_DISPLAYED_EVENT, {"notice_id": notice.id, "language": content.language_code})
        return Response(
            {
                "show": True,
                "notice_id": notice.id,
                "body": _html_to_text(content.html_content),
                "language": content.language_code,
            },
            status=HTTP_200_OK,
        )


class AcknowledgeNotice(APIView):
    """
    POST-only view to acknowledge a single notice for a user

    Path: `/api/notices/v1/acknowledge`

    Returns:
      * 204: OK - Acknowledgment successfully save
      * 400: The requested notice does not exist, or the request didn't include notice data
      * 401: The requesting user is not authenticated.
      * 404: This app is not installed,

    Example request:
    POST /api/notices/v1/acknowledge
    post data: {"notice_id": 10, "acknowledgment_type": "confirmed"}
    """

    authentication_classes = COMMON_AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        Acknowledges the notice for the requesting user
        """
        notice_id = request.data.get("notice_id")
        acknowledgment_type = request.data.get("acknowledgment_type")

        if not notice_id:
            raise ValidationError({"notice_id": "notice_id field required"})

        if not AcknowledgmentResponseTypes.includes_value(acknowledgment_type):
            valid_types = [e.value for e in AcknowledgmentResponseTypes]
            raise ValidationError(
                {"acknowledgment_type": f"acknowledgment_type must be one of the following: {valid_types}"}
            )

        try:
            notice = Notice.objects.get(id=notice_id, active=True)
        except Notice.DoesNotExist as exc:
            raise ValidationError({"notice_id": "notice_id field does not match an existing active notice"}) from exc

        log.info(
            f"Acknowledging notice {notice_id} for user {request.user.id} with "
            f"acknowledgment_type={acknowledgment_type}"
        )
        (acknowledged_notice, _) = AcknowledgedNotice.objects.update_or_create(
            user=request.user, notice=notice, defaults={"response_type": acknowledgment_type}
        )
        snooze_limit = settings.NOTICES_SNOOZE_COUNT_LIMIT
        if snooze_limit is not None and acknowledgment_type == AcknowledgmentResponseTypes.DISMISSED:
            acknowledged_notice.snooze_count = acknowledged_notice.snooze_count + 1
            acknowledged_notice.save()

        # Full-page notices already report this event from the browser (see static/notices/js/utils.js), so only
        # the modal notice, which has no page of its own, is tracked here to avoid counting acknowledgements twice.
        if notice.name == settings.NOTICES_REFUND_POLICY_NOTICE_NAME:
            _emit_tracking_event(
                NOTICE_ACKNOWLEDGED_EVENT,
                {"notice_id": notice.id, "acknowledgment_type": acknowledgment_type},
            )

        # Since this is just an acknowledgment API, we can just return a 204 without any response data.
        return Response(status=HTTP_204_NO_CONTENT)
