"""
Tests for the Notices app's data fetching utilities.
"""
from django.test import TestCase

from notices.data import AcknowledgmentResponseTypes
from notices.selectors import get_visible_notices
from test_utils.factories import AcknowledgedNoticeFactory, NoticeFactory, UserFactory


class TestSelectors(TestCase):
    """
    Test for Selector functions business logic.
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory()

    def test_get_visible_notices(self):
        """
        Happy path. Verifies that "visible" (active and unacknowledged) notice data is returned as expected for a user.
        """
        active_notice = NoticeFactory(active=True)
        active_notice2 = NoticeFactory(active=True)
        active_notice_acked = NoticeFactory(active=True)
        NoticeFactory(active=False)

        AcknowledgedNoticeFactory(
            user=self.user, notice=active_notice_acked, response_type=AcknowledgmentResponseTypes.CONFIRMED
        )

        results = get_visible_notices(self.user)
        assert list(results) == [active_notice, active_notice2]
