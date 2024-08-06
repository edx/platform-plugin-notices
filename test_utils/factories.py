"""
Factories for notices testing.
"""

import datetime

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from notices.models import AcknowledgedNotice, Notice, TranslatedNoticeContent


USER_PASSWORD = "password"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user_%d" % n)
    password = factory.PostGenerationMethodCall("set_password", USER_PASSWORD)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("safe_email")
    is_staff = False
    is_superuser = False
    is_active = True


class NoticeFactory(DjangoModelFactory):
    """
    Notice factory
    """

    class Meta:
        model = Notice

    name = factory.Sequence("Notice number {0}".format)
    active = True


class TranslatedNoticeContentFactory(DjangoModelFactory):
    """
    TranslatedNoticeContent factory
    """

    class Meta:
        model = TranslatedNoticeContent

    notice = factory.SubFactory(NoticeFactory)


class AcknowledgedNoticeFactory(DjangoModelFactory):
    """
    AcknowledgedNotice factory
    """

    class Meta:
        model = AcknowledgedNotice

    user = factory.SubFactory(UserFactory)
    notice = factory.SubFactory(NoticeFactory)
    snooze_count = 0
    created = datetime.datetime.now(datetime.timezone.utc)
