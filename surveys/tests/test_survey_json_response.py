from surveys.survey_json_response import SurveyJsonResponse
from surveys.models import Survey
from unittest.mock import Mock
import pytest


def test_survey_json_response():
    assert SurveyJsonResponse(Mock(spec=Survey))


@pytest.mark.django_db
def test_survey_json_response_value(create_survey, expected_json_survey):
    assert SurveyJsonResponse(Survey.objects.first()).value() == expected_json_survey
