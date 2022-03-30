from abc import ABC, abstractmethod


class ValidationRule(ABC):

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        """"""


class FakeRule(ValidationRule):

    def __init__(self, validate_to: bool = False):
        self._validate_to = validate_to

    def validate(self):
        return self._validate_to
