"""
Database models for notices.
"""
import bleach
from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

User = get_user_model()


class Notice(TimeStampedModel):
    """
    Model to house a notice's content and additional data.

    .. no_pii:
    """

    name = models.CharField(max_length=128, help_text="Name for the notice that needs to be acknowledged")
    html_content = models.TextField(
        help_text=(
            "HTML content to be included in a notice prompt. Allowed tags include (a, b, em, i, span, strong)"
        )
    )
    active = models.BooleanField()
    history = HistoricalRecords(app="notices")

    class Meta:
        """Model metadata."""

        app_label = "notices"

    def save(self, *args, **kwargs):
        """Save method override to remove unsafe tags from html_content first."""
        self.html_content = bleach.clean(self.html_content, tags=["a", "b", "em", "i", "span", "strong"])
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<Notice {self.name}>"


class AcknowledgedNotice(TimeStampedModel):
    """
    Model to track if and when a user has acknowledged the notice.

    Lack of an entry denotes a user has not acknowledged the notice.

    .. no_pii:
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE)

    class Meta:
        """Model metadata."""
        app_label = "notices"

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<AcknowledgedNotice by user {self.user.id} for notice {self.notice.name}>"
