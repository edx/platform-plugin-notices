"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "notices",
    "waffle",
)

LOCALE_PATHS = [
    root("notices", "conf", "locale"),
]

ROOT_URLCONF = "test_utils.test_urls"

SECRET_KEY = "insecure-secret-key"

FEATURES = {"NOTICES_SNOOZE_HOURS": None, "NOTICES_SNOOZE_COUNT_LIMIT": None}

USE_TZ = True
