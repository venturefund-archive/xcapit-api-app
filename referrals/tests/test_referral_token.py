from core.validation_rules.validation_rules import ValidationRules
from referrals.blacklist_tokens import BlacklistTokens
from referrals.referral_token import ReferralToken
from referrals.validation_rules.referral_blacklist_rule import ReferralBlacklistRule


def test_value_access(raw_referral_token):
    assert ReferralToken(raw_referral_token, ValidationRules([])).value() == raw_referral_token


def test_validate(raw_referral_token):
    token = ReferralToken(
        raw_referral_token,
        ValidationRules(
            [ReferralBlacklistRule(BlacklistTokens([raw_referral_token]))]
        )
    )

    assert token.validate() is False
