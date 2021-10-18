"""
Tests for the Notices app's Python API
"""
from django.test import TestCase
from rest_framework.reverse import reverse

from notices.api import get_unacknowledged_notices_for_user
from notices.data import AcknowledgmentResponseTypes
from test_utils.factories import AcknowledgedNoticeFactory, NoticeFactory, UserFactory


class TestPythonApi(TestCase):
    """
    Tests for the Notices app's exposed Python API.
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory()

    def test_unackd_active_notices(self):
        """
        Happy path. Verifies that only active and unack'd notice ids are returned to the caller.
        """
        notice = NoticeFactory(active=True)
        notice2 = NoticeFactory(active=True)
        notice3 = NoticeFactory(active=True)
        notice4 = NoticeFactory(active=True)
        NoticeFactory(active=False)

        AcknowledgedNoticeFactory(user=self.user, notice=notice2, response_type=AcknowledgmentResponseTypes.CONFIRMED)
        AcknowledgedNoticeFactory(user=self.user, notice=notice3, response_type=AcknowledgmentResponseTypes.DISMISSED)

        expected_results = [
            reverse("notices:notice-detail", kwargs={"pk": notice.id}),
            reverse("notices:notice-detail", kwargs={"pk": notice4.id}),
        ]

        results = get_unacknowledged_notices_for_user(self.user)
        assert results == expected_results

    def test_no_unackd_notices_for_user(self):
        """
        Verifies an empty list is returned if a user has no unack'd notices.
        """
        notice = NoticeFactory(active=True)
        AcknowledgedNoticeFactory(user=self.user, notice=notice, response_type=AcknowledgmentResponseTypes.CONFIRMED)

        results = get_unacknowledged_notices_for_user(self.user)
        assert results == []

    def test_no_active_notices_for_user(self):
        """
        Verifies an empty list is returned if a user has no active notices.
        """
        NoticeFactory(active=False)

        results = get_unacknowledged_notices_for_user(self.user)
        assert results == []
