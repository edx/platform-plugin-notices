"""Tests Notices API Views"""
import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from notices.rest_api.v1.views import AcknowledgeNotice, ListUnacknowledgedNotices
from notices.models import AcknowledgedNotice
from notices.data import AcknowledgmentResponseTypes
from test_utils.factories import AcknowledgedNoticeFactory, NoticeFactory, UserFactory


class ListUnacknowledgedNoticesTests(TestCase):
    """Tests for the ListUnacknowledgedNotices view"""

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.request_factory = APIRequestFactory()
        self.view = ListUnacknowledgedNotices.as_view()

    def test_no_notices(self):
        request = self.request_factory.get('/api/v1/unacknowledged/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        # reformat response from list of OrderedDicts to list of Dict
        response = json.loads(json.dumps(response.data))
        assert response == []

    def test_single_notice(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.get('/api/v1/unacknowledged/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert len(response.data) == 1
        assert response.data[0] == {"id": notice_1.id, "name": notice_1.name, "translated_notice_content": []}


    def test_multiple_notices(self):
        notice_1 = NoticeFactory(active=True)
        notice_2 = NoticeFactory(active=True)
        notice_3 = NoticeFactory(active=True)
        request = self.request_factory.get('/api/v1/unacknowledged/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert len(response.data) == 3
        assert {notice["id"] for notice in response.data} == set([notice_1.id, notice_2.id, notice_3.id])

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
        request = self.request_factory.get('/api/v1/unacknowledged/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert len(response.data) == 1
        assert {notice["id"] for notice in response.data} == set([notice_3.id])


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
            '/api/v1/acknowledge/',
            {'notice_id': notice_1.id, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED.value}
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.data is None
        assert response.status_code == 204
        # Verify the acknowledgment made it to the DB
        assert AcknowledgedNotice.objects.filter(user=self.user, notice=notice_1).first() is not None

    def test_no_notice_data(self):
        NoticeFactory(active=True)
        request = self.request_factory.post('/api/v1/acknowledge/')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        assert response.status_code == 400
        json_response_data = json.loads(json.dumps(response.data))
        assert json_response_data == {'notice_id': "notice_id field required"}

    def test_invalid_notice_data(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            '/api/v1/acknowledge/',
            {'notice_id': notice_1.id + 1, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED.value}
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)

        assert response.status_code == 400
        json_response_data = json.loads(json.dumps(response.data))
        assert json_response_data == {'notice_id': "notice_id field does not match an existing active notice"}

    def test_invalid_response_type(self):
        INVALID_CHOICE = "invalid_CHOICE"
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            '/api/v1/acknowledge/',
            {'notice_id': notice_1.id, "acknowledgment_type": INVALID_CHOICE}
        )
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 400
        json_response_data = json.loads(json.dumps(response.data))
        acknowledgment_type_values = [e.value for e in AcknowledgmentResponseTypes]
        assert json_response_data == {
            'acknowledgment_type': f"acknowledgment_type must be one of the following: {acknowledgment_type_values}"
        }

    def test_unauthenticated_call(self):
        notice_1 = NoticeFactory(active=True)
        request = self.request_factory.post(
            '/api/v1/acknowledge/',
            {'notice_id': notice_1.id + 1, "acknowledgment_type": AcknowledgmentResponseTypes.CONFIRMED}
        )
        response = self.view(request)
        assert response.status_code == 401
