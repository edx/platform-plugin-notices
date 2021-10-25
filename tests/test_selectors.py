"""
Tests for the Notices app's data fetching utilities.
"""
import datetime

from django.conf import settings
from django.test import TestCase, override_settings

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

    @override_settings(FEATURES={"NOTICES_SNOOZE_HOURS": 4})
    def test_snoozed_notices(self):
        """
        Tests that snoozed notices are only snoozed for the `NOTICES_SNOOZE_HOURS` amount of time
        """
        SNOOZE_HOURS = settings.FEATURES["NOTICES_SNOOZE_HOURS"]

        active_notice = NoticeFactory(active=True)
        latest_snooze_time = datetime.datetime.now() - datetime.timedelta(hours=SNOOZE_HOURS)

        # acknowledgment an hour older than the snooze limit
        AcknowledgedNoticeFactory(
            user=self.user,
            notice=active_notice,
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            modified=latest_snooze_time - datetime.timedelta(hours=1),
        )

        results = get_visible_notices(self.user)
        assert len(results) == 1
        assert list(results) == [active_notice]

        # acknowledgment an hour newer than the snooze limit
        AcknowledgedNoticeFactory(
            user=self.user,
            notice=active_notice,
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            modified=latest_snooze_time + datetime.timedelta(hours=1),
        )

        results = get_visible_notices(self.user)
        assert len(results) == 0

    @override_settings(FEATURES={"NOTICES_SNOOZE_COUNT_LIMIT": 3})
    def test_snooze_count_notices(self):
        """
        Tests that notices can only be snoozed NOTICES_SNOOZE_COUNT_LIMIT times
        """
        notices_snooze_count_limit = settings.FEATURES["NOTICES_SNOOZE_COUNT_LIMIT"]
        active_notice = NoticeFactory(active=True)

        AcknowledgedNoticeFactory(
            user=self.user,
            notice=active_notice,
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            snooze_count=notices_snooze_count_limit + 1,
        )
        results = get_visible_notices(self.user)
        assert len(results) == 1
        print(results[0].id)
        print(active_notice.id)
        assert list(results) == [active_notice]

        # snooze count >= limit
        AcknowledgedNoticeFactory(
            user=self.user, notice=active_notice, response_type=AcknowledgmentResponseTypes.DISMISSED, snooze_count=1
        )

        results = get_visible_notices(self.user)
        assert len(results) == 0

    @override_settings(FEATURES={"NOTICES_SNOOZE_HOURS": 4, "NOTICES_SNOOZE_COUNT_LIMIT": 3})
    def test_snoozed_notices_with_count(self):
        """
        Tests the interaction between snoozing a notice and the snooze limit.
        """
        SNOOZE_HOURS = settings.FEATURES["NOTICES_SNOOZE_HOURS"]
        notices_snooze_count_limit = settings.FEATURES["NOTICES_SNOOZE_COUNT_LIMIT"]

        active_notice = NoticeFactory(active=True)
        latest_snooze_time = datetime.datetime.now() - datetime.timedelta(hours=SNOOZE_HOURS)

        # acknowledgment an hour older than the snooze limit
        AcknowledgedNoticeFactory(
            user=self.user,
            notice=active_notice,
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            modified=latest_snooze_time - datetime.timedelta(hours=1),
        )

        results = get_visible_notices(self.user)
        assert len(results) == 1
        assert list(results) == [active_notice]

        # acknowledgment an hour newer than the snooze limit, but snooze_limit exceeded
        AcknowledgedNoticeFactory(
            user=self.user,
            notice=active_notice,
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            modified=latest_snooze_time + datetime.timedelta(hours=1),
            snooze_count=notices_snooze_count_limit + 1,
        )

        results = get_visible_notices(self.user)
        assert len(results) == 1
        assert list(results) == [active_notice]

        # acknowledgment an hour newer than the snooze limit
        AcknowledgedNoticeFactory(
            user=self.user,
            notice=active_notice,
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            modified=latest_snooze_time + datetime.timedelta(hours=1),
            snooze_count=1,
        )

        results = get_visible_notices(self.user)
        assert len(results) == 0
