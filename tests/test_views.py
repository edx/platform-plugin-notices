"""Tests Notices API Views"""

import json
from unittest import mock

from django.test import TestCase, override_settings
from edx_toggles.toggles.testutils import override_waffle_flag
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from notices.data import AcknowledgmentResponseTypes
from notices.models import AcknowledgedNotice, TranslatedNoticeContent
from notices.rest_api.v1.views import AcknowledgeNotice, ListUnacknowledgedNotices, RefundPolicyNotice
from notices.toggles import ENABLE_NOTICES, SHOW_REFUND_POLICY_NOTICE
from test_utils.factories import AcknowledgedNoticeFactory, NoticeFactory, TranslatedNoticeContentFactory, UserFactory


class ListUnacknowledgedNoticesTests(TestCase):
    """Tests for the ListUnacknowledgedNotices view"""

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.request_factory = APIRequestFactory()
        self.view = ListUnacknowledgedNotices.as_view()

    @override_waffle_flag(ENABLE_NOTICES, active=True)
    def test_no_notices(self):
        request = self.request_factory.get("/api/v1/unacknowledged/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # reformat response from list of OrderedDicts to list of Dict
        results = response.data["results"]
        assert results == []

    @override_waffle_flag(ENABLE_NOTICES, active=True)
    def test_single_notice(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.get("/api/v1/unacknowledged/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        results = response.data["results"]
        assert len(results) == 1
        assert results == [reverse("notices:notice-detail", kwargs={"pk": notice_1.id}, request=request)]

    @override_waffle_flag(ENABLE_NOTICES, active=True)
    @override_settings(NOTICES_REFUND_POLICY_NOTICE_NAME="Refund Policy Change")
    def test_refund_policy_notice_is_not_listed(self):
        """
        The refund policy notice is shown as a modal, so MFEs must not be redirected to its full page.
        """
        page_notice = NoticeFactory(active=True)
        NoticeFactory(active=True, name="Refund Policy Change")
        request = self.request_factory.get("/api/v1/unacknowledged/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.data["results"] == [
            reverse("notices:notice-detail", kwargs={"pk": page_notice.id}, request=request)
        ]

    @override_waffle_flag(ENABLE_NOTICES, active=True)
    def test_multiple_notices(self):
        notice_1 = NoticeFactory(active=True)
        notice_2 = NoticeFactory(active=True)
        notice_3 = NoticeFactory(active=True)
        request = self.request_factory.get("/api/v1/unacknowledged/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        results = response.data["results"]
        assert len(results) == 3
        # cast to set to avoid ordering issues
        assert set(results) == set(
            [
                reverse("notices:notice-detail", kwargs={"pk": notice_1.id}, request=request),
                reverse("notices:notice-detail", kwargs={"pk": notice_2.id}, request=request),
                reverse("notices:notice-detail", kwargs={"pk": notice_3.id}, request=request),
            ]
        )

    @override_waffle_flag(ENABLE_NOTICES, active=True)
    def test_some_acknowledged(self):
        """
        Test that when a user response to some (but not all) the API only returns the unacknowledged ones

        Also tests that response type is not taken into account when choosing to display
        """
        notice_1 = NoticeFactory(active=True)
        notice_2 = NoticeFactory(active=True)
        notice_3 = NoticeFactory(active=True)
        # acknowledge the middle notice
        AcknowledgedNoticeFactory(user=self.user, notice=notice_2, response_type=AcknowledgmentResponseTypes.CONFIRMED)
        AcknowledgedNoticeFactory(user=self.user, notice=notice_1, response_type=AcknowledgmentResponseTypes.DISMISSED)
        request = self.request_factory.get("/api/v1/unacknowledged/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        results = response.data["results"]
        assert len(results) == 1
        assert results == [
            reverse("notices:notice-detail", kwargs={"pk": notice_3.id}, request=request),
        ]


class AcknowledgeNoticeTests(TestCase):
    """Tests for the AcknowledgeNotice view"""

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.request_factory = APIRequestFactory()
        self.view = AcknowledgeNotice.as_view()

    def test_valid_acknowledgement(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            "/api/v1/acknowledge/",
            {"notice_id": notice_1.id, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED.value},
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.data is None
        assert response.status_code == 204
        # Verify the acknowledgment made it to the DB
        assert AcknowledgedNotice.objects.filter(user=self.user, notice=notice_1).first() is not None

    @override_settings(NOTICES_REFUND_POLICY_NOTICE_NAME="Refund Policy Change")
    def test_tracking_event_only_for_refund_policy_notice(self):
        """
        Full-page notices report acknowledgements from the browser, so only the modal notice is tracked here.
        """
        page_notice = NoticeFactory(active=True)
        modal_notice = NoticeFactory(active=True, name="Refund Policy Change")

        for notice, expect_event in ((page_notice, False), (modal_notice, True)):
            request = self.request_factory.post(
                "/api/v1/acknowledge/",
                {"notice_id": notice.id, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED.value},
            )
            force_authenticate(request, user=self.user)
            with mock.patch("notices.rest_api.v1.views._emit_tracking_event") as emit:
                assert self.view(request).status_code == 204
            if expect_event:
                emit.assert_called_once_with(
                    "edx.bi.user.acknowledged_notice",
                    {"notice_id": notice.id, "acknowledgment_type": "confirmed"},
                )
            else:
                emit.assert_not_called()

    def test_no_notice_data(self):
        NoticeFactory(active=True)
        request = self.request_factory.post("/api/v1/acknowledge/")
        force_authenticate(request, user=self.user)
        response = self.view(request)

        assert response.status_code == 400
        json_response_data = json.loads(json.dumps(response.data))
        assert json_response_data == {"notice_id": "notice_id field required"}

    def test_invalid_notice_data(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            "/api/v1/acknowledge/",
            {"notice_id": notice_1.id + 1, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED.value},
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)

        assert response.status_code == 400
        json_response_data = json.loads(json.dumps(response.data))
        assert json_response_data == {"notice_id": "notice_id field does not match an existing active notice"}

    def test_invalid_response_type(self):
        INVALID_CHOICE = "invalid_CHOICE"
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            "/api/v1/acknowledge/", {"notice_id": notice_1.id, "acknowledgment_type": INVALID_CHOICE}
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 400
        json_response_data = json.loads(json.dumps(response.data))
        acknowledgment_type_values = [e.value for e in AcknowledgmentResponseTypes]
        assert json_response_data == {
            "acknowledgment_type": f"acknowledgment_type must be one of the following: {acknowledgment_type_values}"
        }

    def test_unauthenticated_call(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            "/api/v1/acknowledge/",
            {"notice_id": notice_1.id + 1, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED},
        )
        response = self.view(request)
        assert response.status_code == 401


@override_settings(FEATURES={"NOTICES_FALLBACK_LANGUAGE": "en"})
class RefundPolicyNoticeTests(TestCase):
    """Tests for the RefundPolicyNotice view"""

    NOTICE_NAME = "Refund Policy Change"

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.request_factory = APIRequestFactory()
        self.view = RefundPolicyNotice.as_view()
        self.notice = NoticeFactory(name=self.NOTICE_NAME, active=True)
        TranslatedNoticeContentFactory(notice=self.notice, language_code="en", html_content="<p>English body</p>")
        TranslatedNoticeContentFactory(notice=self.notice, language_code="es", html_content="<p>Cuerpo</p>")

    def _get(self, user=None, **extra):
        request = self.request_factory.get("/api/v1/refund-policy", **extra)
        if user is not None:
            force_authenticate(request, user=user)
        return self.view(request)

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=False)
    def test_flag_off(self):
        response = self._get(self.user)
        assert response.status_code == 200
        assert response.data == {"show": False}

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_unauthenticated(self):
        assert self._get().status_code == 401

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_unacknowledged_notice_is_shown(self):
        response = self._get(self.user)
        assert response.data == {"show": True, "notice_id": self.notice.id, "body": "English body", "language": "en"}

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_body_keeps_paragraph_breaks_and_drops_markup(self):
        TranslatedNoticeContent.objects.filter(notice=self.notice, language_code="en").update(
            html_content="<h2>Title</h2><p>First <b>paragraph</b> &amp; more.</p><p>Second<br>line</p>"
        )
        body = self._get(self.user).data["body"]
        assert body == "Title\nFirst paragraph & more.\nSecond\nline"

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_user_joined_after_launch_still_sees_notice(self):
        self.notice.launch_date = self.user.date_joined
        self.notice.save()
        assert self._get(self.user).data["show"] is True

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_confirmed_notice_is_hidden(self):
        AcknowledgedNoticeFactory(
            user=self.user, notice=self.notice, response_type=AcknowledgmentResponseTypes.CONFIRMED
        )
        assert self._get(self.user).data == {"show": False}

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_dismissed_notice_is_still_shown(self):
        AcknowledgedNoticeFactory(
            user=self.user, notice=self.notice, response_type=AcknowledgmentResponseTypes.DISMISSED
        )
        assert self._get(self.user).data["show"] is True

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_inactive_or_missing_notice(self):
        self.notice.active = False
        self.notice.save()
        assert self._get(self.user).data == {"show": False}

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_translated_content(self):
        response = self._get(self.user, HTTP_ACCEPT_LANGUAGE="es")
        assert response.data["body"] == "Cuerpo"
        assert response.data["language"] == "es"

    @override_waffle_flag(SHOW_REFUND_POLICY_NOTICE, active=True)
    def test_falls_back_to_default_language(self):
        response = self._get(self.user, HTTP_ACCEPT_LANGUAGE="fr")
        assert response.data["language"] == "en"
        assert response.data["body"] == "English body"
