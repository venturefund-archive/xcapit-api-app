import pytest
from io import StringIO
from django.core.management import call_command
from surveys.models import Survey, Question, Choice


@pytest.mark.django_db
def test_command_load_investor_test_survey():
    out = StringIO()
    call_command('load_investor_test_survey', stdout=out)
    assert 'Successful data upload' in out.getvalue()
    survey = Survey.objects.get(name='investor_test')
    assert survey
    questions = Question.objects.filter(survey=survey)
    assert questions.count() == 5
    assert questions[2].order == 3
    all_choices = Choice.objects.filter(question__survey=survey)
    assert all_choices.count() == 18
