import pytest
from core.validation_rules.validation_rule import FakeRule
from core.validation_rules.validation_rules import ValidationRules


def test_new():
    validation_rules = ValidationRules(rules=[FakeRule()])

    assert validation_rules


def test_validate_false_when_rules_is_empty():
    validation_rules = ValidationRules(rules=[])

    assert validation_rules.validate() is False


@pytest.mark.parametrize('rules, expected_value', [[[], True], [[FakeRule()], False]])
def test_emtpy(rules, expected_value):
    validation_rules = ValidationRules(rules)

    assert validation_rules.empty() is expected_value


@pytest.mark.parametrize('expected_value', [True, False])
def test_validate_simple_rule(expected_value):
    validation_rules = ValidationRules(rules=[FakeRule(validate_to=expected_value)])

    assert validation_rules.validate() is expected_value


@pytest.mark.parametrize('first_rule, second_rule, expected_value', [
    [True, True, True],
    [True, False, False],
    [False, False, False],
    [False, True, False],
])
def test_validate_multiples_rules(first_rule, second_rule, expected_value):
    validation_rules = ValidationRules(rules=[FakeRule(validate_to=first_rule), FakeRule(validate_to=second_rule)])

    assert validation_rules.validate() is expected_value
