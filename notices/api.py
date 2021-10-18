"""
Python API for Notice data.
"""
from rest_framework.reverse import reverse

from notices.selectors import get_visible_notices


def get_unacknowledged_notices_for_user(user, in_app=False, request=None):
    """
    Retrieve a list of all unacknowledged (active) Notices for a given user.

    Returns:
        (list): A (text) list of URLs to the unack'd Notices.
    """
    unacknowledged_active_notices = get_visible_notices(user)

    urls = []
    if unacknowledged_active_notices:
        urls = [
            reverse("notices:notice-detail", kwargs={"pk": notice.id}, request=request)
            + ("?mobile=true" if in_app else "")
            for notice in unacknowledged_active_notices
        ]

    return urls
