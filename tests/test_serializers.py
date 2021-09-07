"""Tests for the Notices plugin serializers """
import json

from django.test import TestCase

from notices.rest_api.v1.serializers import NoticeSerializer
from test_utils.factories import NoticeFactory, TranslatedNoticeContentFactory


class TestNoticeSerializer(TestCase):
    """
    Tests for NoticeSerializer

    Since the NoticeSerializer inlines the TranslateNoticeContentSerializer and the serializer is read only, we only
    need to verify that the correct format is being returned. No need to post validation, etc.
    """

    def testResponseFormat(self):
        """Test that all expected data is in the response"""
        first_notice = NoticeFactory()
        second_notice = NoticeFactory()
        first_content_for_first_notice = TranslatedNoticeContentFactory(
            notice=first_notice,
            language_code="en-US",
            html_content="This is a <b>test</b> notice."
        )
        second_content_for_first_notice = TranslatedNoticeContentFactory(
            notice=first_notice,
            language_code="es-ES",
            # This was an auto translation, sorry if it's wrong
            html_content="Este es un aviso de <b>prueba</b>."
        )
        first_content_for_second_notice = TranslatedNoticeContentFactory(
            notice=second_notice,
            language_code="en-US",
            html_content="This is a <i>second</i> <b>test</b> notice."
        )
        notices = [first_notice, second_notice]

        expected_content = [
            {
                "id": first_notice.id,
                "name": first_notice.name,
                "translated_notice_content": [
                    {
                        "language_code": first_content_for_first_notice.language_code,
                        "html_content": first_content_for_first_notice.html_content
                    },
                    {
                        "language_code": second_content_for_first_notice.language_code,
                        "html_content": second_content_for_first_notice.html_content
                    },
                ]
            },
            {
                "id": second_notice.id,
                "name": second_notice.name,
                "translated_notice_content": [
                    {
                        "language_code": first_content_for_second_notice.language_code,
                        "html_content": first_content_for_second_notice.html_content
                    },
                ]
            }
        ]
        serializer = NoticeSerializer(notices, many=True)
        # json required because serializer.data is an OrderedDict and this is
        # the easiest way to go from OrderedDict->Dict
        assert expected_content == json.loads(json.dumps(serializer.data))
