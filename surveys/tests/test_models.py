from surveys.models import Survey, Question, Choice, QuestionTranslation
from django.db import IntegrityError
import pytest


@pytest.mark.django_db
def test_create_survey_with_questions_and_answers(create_survey):
    survey = Survey.objects.get(name='investor_test')
    questions = survey.questions.all()

    assert survey
    assert len(survey.questions.all()) == 3
    for question in questions:
        choices = question.choices.all()
        assert len(question.translated_questions.all()) == 2
        assert len(question.choices.all()) == 3

        for choice in choices:
            assert len(choice.translated_choices.all()) == 2


@pytest.mark.django_db
def test_create_question_with_same_order_in_same_survey_raises_exception(create_survey):
    with pytest.raises(IntegrityError):
        Question.objects.create(survey=Survey.objects.get(name='investor_test'), order=0)


@pytest.mark.django_db
def test_create_question_with_same_order_in_new_survey_ok(create_survey):
    different_survey = Survey.objects.create(name='SurveyTwo')
    assert Question.objects.create(survey=different_survey, order=0)
