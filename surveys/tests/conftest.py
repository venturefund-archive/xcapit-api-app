from surveys.models import Choice, Question, Survey
import pytest
import json


@pytest.fixture
def create_survey():
    questions = ['Lorem Ipsum', 'dolor sit amet', 'consectetur adipiscing elit']
    choices = [{'text': 'ChoiceOne', 'value': 1},
               {'text': 'ChoiceTwo', 'value': 2},
               {'text': 'ChoiceThree', 'value': 3}]

    survey = Survey.objects.create(name='investor_test')
    for question in questions:
        created_question = Question.objects.create(survey=survey, text=question)
        for choice in choices:
            Choice.objects.create(question=created_question, text=choice['text'], value=choice['value'])


@pytest.fixture
def expected_survey():
    return [
        {
            "text": "Lorem Ipsum",
            "order": 0,
            "options": [
                {"text": "ChoiceOne", "points": 1},
                {"text": "ChoiceTwo", "points": 2},
                {"text": "ChoiceThree", "points": 3}
            ]
        },
        {
            "text": "dolor sit amet",
            "order": 1,
            "options": [
                {"text": "ChoiceOne", "points": 1},
                {"text": "ChoiceTwo", "points": 2},
                {"text": "ChoiceThree", "points": 3}
            ]
        },
        {
            "text": "consectetur adipiscing elit",
            "order": 2,
            "options": [
                {"text": "ChoiceOne", "points": 1},
                {"text": "ChoiceTwo", "points": 2},
                {"text": "ChoiceThree", "points": 3}
            ]
        }
    ]


@pytest.fixture
def expected_question_json_response():
    return {
        "text": "Lorem Ipsum",
        "order": 0,
        "options": [
            {"text": "ChoiceOne", "points": 1},
            {"text": "ChoiceTwo", "points": 2},
            {"text": "ChoiceThree", "points": 3}
        ]
    }
