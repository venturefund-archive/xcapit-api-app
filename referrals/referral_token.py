from core.validation_rules.validation_rule import ValidationRule
from core.validation_rules.validation_rules import ValidationRules


class ReferralToken(ValidationRule):

    def __init__(self, a_raw_token: str, rules: ValidationRules):
        self._rules = rules
        self._a_raw_token = a_raw_token

    def value(self):
        return self._a_raw_token

    def validate(self) -> bool:
        return self._rules.validate(self)
