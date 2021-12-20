from surveys.models import Survey, Question, Choice
from django.db import IntegrityError
import pytest


@pytest.mark.django_db
def test_create_survey_with_questions_and_answers(create_survey):
    assert Survey.objects.get(name='investor_test')
    assert len(Question.objects.all()) == 3
    assert len(Choice.objects.all()) == 9


@pytest.mark.django_db
def test_create_question_with_same_order_in_same_survey_raises_exception(create_survey):
    with pytest.raises(IntegrityError):
        Question.objects.create(survey=Survey.objects.get(name='investor_test'), text='test', order=0)


@pytest.mark.django_db
def test_create_question_with_same_order_in_new_survey_ok(create_survey):
    different_survey = Survey.objects.create(name='SurveyTwo')
    assert Question.objects.create(survey=different_survey, text='test', order=0)
