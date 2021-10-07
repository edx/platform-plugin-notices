"""
Functions to add context to LMS pages via the plugins context feature.
"""
from django.conf import settings

from .api import get_unacknowledged_notices_for_user


def get_dashboard_context(existing_context):
    """
    Return additional context for the course dashboard.
    """
    user = existing_context.get("user")

    data = None
    if settings.FEATURES.get("ENABLE_NOTICES") and user:
        data = get_unacknowledged_notices_for_user(user)

    return {
        "unacknowledged_notices": data,
    }
