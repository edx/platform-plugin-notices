"""This file houses all the toggles, namely waffle switches and flags."""

from edx_toggles.toggles import WaffleFlag


# .. toggle_name: notices.enable_notices
# .. toggle_implementation: WaffleFlag
# .. toggle_default: False
# .. toggle_description: If enabled, the unacknowledged notices API will return notices the user hasn't acknowledged
# .. toggle_use_cases: opt_in
# .. toggle_creation_date: 2021-10-07
ENABLE_NOTICES = WaffleFlag("notices.enable_notices", module_name=__name__, log_prefix="notices")

# .. toggle_name: commerce.show_refund_policy_change_notice
# .. toggle_implementation: WaffleFlag
# .. toggle_default: False
# .. toggle_description: If enabled, the refund policy notice API returns the refund policy change notice to
#   learners who have not yet acknowledged it. Shares its name with the flag defined in edx-platform
#   (lms/djangoapps/commerce/toggles.py); this plugin is where the flag is read for the notice API.
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2026-11-13
# .. toggle_target_removal_date: None
# .. toggle_warning: Turn this on before commerce.enable_refund_policy_change so learners see the notice before the
#   policy applies. Set to Everyone (Yes or No) only, so every learner gets the same answer.
# .. toggle_tickets: LP-1413, LP-1429
SHOW_REFUND_POLICY_NOTICE = WaffleFlag(
    "commerce.show_refund_policy_change_notice", module_name=__name__, log_prefix="notices"
)
