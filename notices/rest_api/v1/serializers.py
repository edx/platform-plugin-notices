"""Serializers for the notices v1 rest API"""
from rest_framework import serializers

from notices.models import Notice, TranslatedNoticeContent


class TranslateNoticeContentSerializer(serializers.ModelSerializer):
    """Serializer for translated notice content"""
    class Meta:
        model = TranslatedNoticeContent
        fields = ('language_code', 'html_content')


class NoticeSerializer(serializers.ModelSerializer):
    """Serializer for notice"""
    translated_notice_content = TranslateNoticeContentSerializer(many=True, read_only=True)

    class Meta:
        model = Notice
        fields = ('id', 'name', 'translated_notice_content')
