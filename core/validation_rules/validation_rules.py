from typing import List
from core.validation_rules.validation_rule import ValidationRule


class ValidationRules(ValidationRule):

    def __init__(self, rules: List[ValidationRule]):
        self._rules = rules

    def empty(self) -> bool:
        return not bool(self._rules)

    def validate(self, *args, **kwargs) -> bool:
        result = not self.empty()
        for rule in self._rules:
            if not rule.validate(*args, **kwargs):
                result = False
                break
        return result
