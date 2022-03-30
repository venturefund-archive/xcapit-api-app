import pytest
from referrals.referral_token import ReferralToken
from core.validation_rules.validation_rules import ValidationRules
from referrals.blacklist_tokens import BlacklistTokens
from referrals.validation_rules.referral_blacklist_rule import ReferralBlacklistRule


@pytest.fixture
def blacklist_tokens(raw_referral_token):
    return BlacklistTokens([raw_referral_token])


@pytest.fixture
def referral_token():
    def rt(raw_token):
        return ReferralToken(raw_token, ValidationRules([]))

    return rt


def test_new(blacklist_tokens):
    assert ReferralBlacklistRule(blacklist_tokens)


def test_validation_false(raw_referral_token, blacklist_tokens, referral_token):
    rule = ReferralBlacklistRule(blacklist_tokens)

    assert rule.validate(referral_token(raw_referral_token)) is False


def test_validation_true(blacklist_tokens, referral_token):
    rule = ReferralBlacklistRule(blacklist_tokens)

    assert rule.validate(referral_token('any_referral')) is True
