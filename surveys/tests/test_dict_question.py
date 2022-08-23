from surveys.dict_question import DictQuestion
from surveys.models import Question
from unittest.mock import Mock
import pytest


def test_question_json_response():
    assert DictQuestion(Mock(spec=Question), 'es')


@pytest.mark.django_db
def test_spanish_question_json_response_value(create_survey, expected_spanish_question_json_response):
    assert DictQuestion(Question.objects.first(), 'es').value() == expected_spanish_question_json_response


@pytest.mark.django_db
def test_english_question_json_response_value(create_survey, expected_english_question_json_response):
    assert DictQuestion(Question.objects.first(), 'en').value() == expected_english_question_json_response
