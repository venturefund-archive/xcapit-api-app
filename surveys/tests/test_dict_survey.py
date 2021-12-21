from surveys.dict_survey import DictSurvey
from surveys.models import Survey
from unittest.mock import Mock
import pytest


def test_survey_json_response():
    assert DictSurvey(Mock(spec=Survey))


@pytest.mark.django_db
def test_survey_json_response_value(create_survey, expected_survey):
    assert DictSurvey(Survey.objects.first()).value() == expected_survey
