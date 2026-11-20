"""Common settings for notices app"""


def plugin_settings(settings):
    """Settings for the notices app"""
    settings.NOTICES_REDIRECT_ALLOWLIST = []
    settings.NOTICES_DEFAULT_REDIRECT_URL = "http://www.example.com"
    settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"] = "en"
    settings.FEATURES["NOTICES_SEGMENT_KEY"] = None
    settings.NOTICES_SNOOZE_HOURS = None
    settings.NOTICES_SNOOZE_COUNT_LIMIT = None
    settings.NOTICES_MAX_SNOOZE_DAYS = None
    settings.NOTICES_ENABLE_MOBILE = True
    # Name of the Notice served by the refund policy notice API (/notices/api/v1/refund-policy)
    settings.NOTICES_REFUND_POLICY_NOTICE_NAME = "Refund Policy Change"
