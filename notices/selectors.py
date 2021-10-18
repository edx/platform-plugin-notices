"""
Utility functions for pulling Notice data.
"""
from django.db.models.query_utils import Q

from notices.models import AcknowledgedNotice, Notice


def get_active_notices():
    """
    Return a QuerySet of all active Notices.
    """
    return Notice.objects.filter(active=True)


def get_acknowledged_notices_for_user(user):
    """
    Return a QuerySet of all acknowledged Notices for a given user.
    """
    return AcknowledgedNotice.objects.filter(user=user)


def get_visible_notices(user):
    """
    Return a QuerySet of all active and unacknowledged Notices for a given user.
    """
    active_notices = get_active_notices()
    acknowledged_notices = get_acknowledged_notices_for_user(user)

    query = Q(id__in=[acked.notice.id for acked in acknowledged_notices])

    return active_notices.exclude(query)
