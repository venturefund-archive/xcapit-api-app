from surveys.dict_survey import DictSurvey
from surveys.models import Survey
from unittest.mock import Mock
import pytest


def test_survey_json_response():
    assert DictSurvey(Mock(spec=Survey), 'es')


@pytest.mark.django_db
def test_spanish_survey_json_response_value(create_survey, expected_spanish_survey):
    assert DictSurvey(Survey.objects.first(), 'es').value() == expected_spanish_survey


@pytest.mark.django_db
def test_english_survey_json_response_value(create_survey, expected_english_survey):
    assert DictSurvey(Survey.objects.first(), 'en').value() == expected_english_survey
