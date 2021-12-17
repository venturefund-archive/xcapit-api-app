from surveys.models import Survey, Question, Choice
from django.db import IntegrityError
import pytest


@pytest.mark.django_db
def test_create_survey_with_questions_and_answers(create_survey):
    assert Survey.objects.get(name='investor_test')
    assert len(Question.objects.all()) == 3
    assert len(Choice.objects.all()) == 9


@pytest.mark.django_db
def test_choice_to_dict(create_survey):
    choice_dict = Choice.objects.first().to_dict()
    assert choice_dict == {"text": "ChoiceOne", "points": 1}


@pytest.mark.django_db
def test_question_to_dict(create_survey):
    question_dict = Question.objects.first().to_dict()
    assert question_dict == {
        "text": "Lorem Ipsum",
        "order": 0,
        "options": [
            {"text": "ChoiceOne", "points": 1},
            {"text": "ChoiceTwo", "points": 2},
            {"text": "ChoiceThree", "points": 3}
        ]
    }


@pytest.mark.django_db
def test_survey_to_json(create_survey, expected_json_survey):
    survey = Survey.objects.get(name='investor_test').to_json()
    assert survey == expected_json_survey


@pytest.mark.django_db
def test_create_question_with_same_order_in_same_survey_raises_exception(create_survey):
    with pytest.raises(IntegrityError):
        Question.objects.create(survey=Survey.objects.get(name='investor_test'), text='test', order=0)


@pytest.mark.django_db
def test_create_question_with_same_order_in_new_survey_ok(create_survey):
    different_survey = Survey.objects.create(name='SurveyTwo')
    assert Question.objects.create(survey=different_survey, text='test', order=0)
