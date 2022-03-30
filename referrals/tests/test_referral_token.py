import pytest
from core.validation_rules.validation_rules import ValidationRules
from referrals.blacklist_tokens import BlacklistTokens
from referrals.referral_token import ReferralToken
from referrals.validation_rules.referral_blacklist_rule import ReferralBlacklistRule


def test_value_access(raw_token):
    assert ReferralToken(raw_token, ValidationRules([])).value() == raw_token


def test_validate(raw_token):
    token = ReferralToken(
        raw_token,
        ValidationRules(
            [ReferralBlacklistRule(BlacklistTokens([raw_token]))]
        )
    )

    assert token.validate() is False
