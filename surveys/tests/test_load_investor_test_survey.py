import pytest
from io import StringIO
from django.core.management import call_command
from surveys.models import Survey, Question, Choice, QuestionTranslation, ChoiceTranslation


@pytest.mark.django_db
def test_command_load_investor_test_survey():
    out = StringIO()
    call_command('load_investor_test_survey', stdout=out)
    assert 'Successful data upload' in out.getvalue()
    survey = Survey.objects.get(name='investor_test')
    assert survey
    assert Question.objects.filter(survey=survey).count() == 5
    assert QuestionTranslation.objects.filter(question__survey=survey).count() == 10
    assert Choice.objects.filter(question__survey=survey).count() == 18
    assert ChoiceTranslation.objects.filter(choice__question__survey=survey).count() == 36
