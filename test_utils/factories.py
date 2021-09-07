"""
Factories for notices testing.
"""
import factory
from factory.django import DjangoModelFactory

from notices.models import Notice, TranslatedNoticeContent

class NoticeFactory(DjangoModelFactory):
    """
    Notice factory to be used by TranslatedNoticeContent
    """

    class Meta:
        model = Notice

    name = factory.Sequence(u"Notice number {0}".format)
    active = True


class TranslatedNoticeContentFactory(DjangoModelFactory):
    """
    TranslatedNoticeContent factory
    """

    class Meta:
        model = TranslatedNoticeContent

    notice = factory.SubFactory(NoticeFactory)
