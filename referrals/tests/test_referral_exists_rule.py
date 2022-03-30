import pytest
from referrals.referral_token import ReferralToken
from core.validation_rules.validation_rules import ValidationRules
from referrals.validation_rules.referral_exists_rule import ReferralExistsRule


def test_new(raw_token):
    assert ReferralExistsRule(False)


@pytest.mark.parametrize('exists_db_referral_user, raw_token_, expected_result', [
    [False, 'test', False],
    [True, 'test', True],
])
def test_validate(exists_db_referral_user, raw_token_, expected_result):
    rule = ReferralExistsRule(exists_db_referral_user)

    assert rule.validate(ReferralToken(raw_token_, ValidationRules([]))) is expected_result
