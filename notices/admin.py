"""Admin pages for the notices app."""
from django.contrib import admin

from .models import AcknowledgedNotice, Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass


@admin.register(AcknowledgedNotice)
class AcknowledgedNoticeAdmin(admin.ModelAdmin):
    pass
