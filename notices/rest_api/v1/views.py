"""API views for the notices app"""

from django.core.exceptions import ValidationError
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from notices.models import AcknowledgedNotice, Notice
from notices.rest_api.v1.serializers import NoticeSerializer


class ListUnacknowledgedNotices(APIView):
    """
    Read only view to list all notices that the user hasn't acknowledged.

    Path: `/api/notices/v1/unacknowledged`

    Returns:
      * 200: OK - Contains a list of active unacknowledged notices the user still needs to see
      * 401: The requesting user is not authenticated.
      * 404: This app is not installed

    Example:
    {
        "results": [
            {
                "id": 1
                "name": "First notice",
                "translated_notice_content": [
                    {
                        "language_code": "en-US",
                        "html_content": "<b>Hello</b>"
                    },
                    {
                        "language_code": "es-ES",
                        "html_content": "<i>Hola</i>"
                    }
                ]
            }
        ]
    }
    """
    authentication_classes = (JwtAuthentication, SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Return a list of all active unacknowledged notices for the user
        """
        acknowledged_notices = AcknowledgedNotice.objects.filter(user=request.user)
        unacknowledged_active_notices = Notice.objects.filter(active=True).exclude(
            id__in=[acked.notice.id for acked in acknowledged_notices]
        )
        serializer = NoticeSerializer(unacknowledged_active_notices, many=True, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)


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
    post data: {notice_id: 10}
    """
    authentication_classes = (JwtAuthentication, SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        Acknowledges the notice for the requesting user
        """
        notice_id = request.data.get("notice_id")
        if not notice_id:
            raise ValidationError("notice_id required to acknowledge notice")

        try:
            notice = Notice.objects.get(id=notice_id, active=True)
        except Notice.DoesNotExist as exc:
            raise ValidationError("Request notice does not exist or is not active") from exc

        AcknowledgedNotice.objects.update_or_create(user=request.user, notice=notice)
        # Since this is just an acknowledgment API, we can just return a 200 OK.
        return Response(status=HTTP_204_NO_CONTENT)
