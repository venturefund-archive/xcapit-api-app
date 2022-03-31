from core.validation_rules.validation_rule import ValidationRule
from referrals.referral_token import ReferralToken


class ReferralExistsRule(ValidationRule):

    def __init__(self, exists_db_referral_user: bool):
        self._exists_db_referral_user = exists_db_referral_user

    def validate(self, a_referral_token: ReferralToken) -> bool:
        return self._exists_db_referral_user if a_referral_token.value() else True
