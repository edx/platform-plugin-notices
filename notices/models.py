"""
Database models for notices.
"""
import bleach
from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from notices.data import AcknowledgmentResponseTypes


User = get_user_model()


class Notice(TimeStampedModel):
    """
    Model to house a notice's content and additional data.

    .. no_pii:
    """

    name = models.CharField(max_length=128, help_text="Name for the notice that needs to be acknowledged")
    active = models.BooleanField()
    history = HistoricalRecords(app="notices")

    class Meta:
        """Model metadata."""

        app_label = "notices"

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<Notice {self.name}>"


class TranslatedNoticeContent(TimeStampedModel):
    """
    A model to house a translated html notice and the language it's translated into.

    A Notice may have multiple TranslatedNoticeContents, with no more than one for each
    language.

    .. no_pii:
    """

    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="translated_notice_content")
    language_code = models.CharField(max_length=10, help_text="The IETF BCP 47 language code for this translation")
    html_content = models.TextField(
        help_text=(
            "HTML content to be included in a notice prompt. Allowed tags include (a, b, em, i, img, span, strong)"
        )
    )
    history = HistoricalRecords(app="notices")

    class Meta:
        """Model metadata."""

        app_label = "notices"
        unique_together = ["notice", "language_code"]

    def save(self, *args, **kwargs):
        """Save method override to remove unsafe tags from html_content first."""
        self.html_content = bleach.clean(self.html_content, tags=["a", "b", "em", "i", "img", "span", "strong"])
        super().save(*args, **kwargs)


class AcknowledgedNotice(TimeStampedModel):
    """
    Model to track if and when a user has acknowledged the notice.

    Lack of an entry denotes a user has not acknowledged the notice.

    .. no_pii:
    """

    RESPONSE_TYPE_CHOICES = [
        (AcknowledgmentResponseTypes.CONFIRMED.value, "Confirmed"),
        (AcknowledgmentResponseTypes.DISMISSED.value, "Dismissed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notice_acknowledgments")
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name="acknowledgments")
    response_type = models.CharField(max_length=32, choices=RESPONSE_TYPE_CHOICES)

    class Meta:
        """Model metadata."""

        app_label = "notices"

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<AcknowledgedNotice by user {self.user.id} for notice {self.notice.name}>"
