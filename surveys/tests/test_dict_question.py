from surveys.dict_question import DictQuestion
from surveys.models import Question
from unittest.mock import Mock
import pytest


def test_question_json_response():
    assert DictQuestion(Mock(spec=Question))


@pytest.mark.django_db
def test_question_json_response_value(create_survey, expected_question_json_response):
    assert DictQuestion(Question.objects.first()).value() == expected_question_json_response
