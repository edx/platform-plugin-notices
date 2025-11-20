"""Production settings for notices app"""


def plugin_settings(settings):
    """Settings for the notices app"""
    settings.NOTICES_REDIRECT_ALLOWLIST = settings.ENV_TOKENS.get(
        "NOTICES_REDIRECT_ALLOWLIST", settings.NOTICES_REDIRECT_ALLOWLIST
    )
    settings.NOTICES_DEFAULT_REDIRECT_URL = settings.ENV_TOKENS.get(
        "NOTICES_DEFAULT_REDIRECT_URL", settings.NOTICES_DEFAULT_REDIRECT_URL
    )
    settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"] = settings.ENV_TOKENS.get(
        "NOTICES_FALLBACK_LANGUAGE", settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"]
    )
    settings.NOTICES_SNOOZE_HOURS = settings.ENV_TOKENS.get("NOTICES_SNOOZE_HOURS", settings.NOTICES_SNOOZE_HOURS)
    settings.NOTICES_SNOOZE_COUNT_LIMIT = settings.ENV_TOKENS.get(
        "NOTICES_SNOOZE_COUNT_LIMIT", settings.NOTICES_SNOOZE_COUNT_LIMIT
    )
    settings.FEATURES["NOTICES_SEGMENT_KEY"] = settings.AUTH_TOKENS.get(
        "SEGMENT_KEY", settings.FEATURES["NOTICES_SEGMENT_KEY"]
    )
    settings.NOTICES_MAX_SNOOZE_DAYS = settings.ENV_TOKENS.get(
        "NOTICES_MAX_SNOOZE_DAYS", settings.NOTICES_MAX_SNOOZE_DAYS
    )
    settings.NOTICES_ENABLE_MOBILE = settings.ENV_TOKENS.get("NOTICES_ENABLE_MOBILE", settings.NOTICES_ENABLE_MOBILE)
