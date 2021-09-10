#!/usr/bin/env python
"""
Tests for the `platform-plugin-notices` models module.
"""
from django.test import TestCase

from test_utils.factories import NoticeFactory, TranslatedNoticeContentFactory


class TestTranslatedNoticeContent(TestCase):
    """
    Tests of the TranslatedNoticeContent model.
    """

    def setUp(self):
        super().setUp()
        self.notice = NoticeFactory()

    def test_save_clean_tags(self):
        """Tests to make sure unclean html tags get cleaned and allowed ones stay"""
        unclean_content = """
            <div>Content</div>
            <b>Bold</b>
            <script>alert("Gotcha")</script>
            <a href="http://www.example.com">Link</a>
        """
        expected_content = """
            &lt;div&gt;Content&lt;/div&gt;
            <b>Bold</b>
            &lt;script&gt;alert("Gotcha")&lt;/script&gt;
            <a href="http://www.example.com">Link</a>
        """
        translated_content = TranslatedNoticeContentFactory(
            notice=self.notice, language_code="en-US", html_content=unclean_content
        )
        assert translated_content.html_content == expected_content
