from surveys.dict_choice import DictChoice
from surveys.models import Choice
from unittest.mock import Mock
import pytest


def test_dict_choice():
    assert DictChoice(Mock(spec=Choice))


@pytest.mark.django_db
def test_dict_choice_value(create_survey):
    assert DictChoice(Choice.objects.first()).value() == {"text": "ChoiceOne", "points": 1}
