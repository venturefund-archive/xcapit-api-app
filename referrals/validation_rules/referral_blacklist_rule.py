from referrals.referral_token import ReferralToken
from core.validation_rules.validation_rule import ValidationRule
from referrals.tests.test_referral_blacklist_rule import BlacklistTokens


class ReferralBlacklistRule(ValidationRule):

    def __init__(self, blacklist_tokens: BlacklistTokens):
        self._blacklist_tokens = blacklist_tokens

    def validate(self, a_referral_token: ReferralToken) -> bool:
        return a_referral_token.value() not in self._blacklist_tokens.value()
