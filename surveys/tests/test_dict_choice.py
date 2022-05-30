from surveys.dict_choice import DictChoice
from surveys.models import Choice
from unittest.mock import Mock
import pytest


def test_dict_choice():
    assert DictChoice(Mock(spec=Choice), 'es')


@pytest.mark.django_db
@pytest.mark.parametrize('language, expected_result',
                         [['es', {"text": "OpciónUno", "points": 1}],
                          ['en', {"text": "ChoiceOne", "points": 1}]])
def test_dict_choice_value(create_survey, language, expected_result):
    assert DictChoice(Choice.objects.first(), language).value() == expected_result
