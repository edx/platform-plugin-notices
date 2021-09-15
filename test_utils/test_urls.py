"""
Overrides the base URL config for tests.

Used by setting `ROOT_URLCONF = "test_utils.test_urls"` in test_settings.py.
Allows us to namespace all URLs as "notices" in the same way the plugin would in LMS.
"""
from django.conf.urls import include, url
from django.urls import path


urlpatterns = [
    path("", include(("notices.urls", "root"), namespace="notices")),
]
