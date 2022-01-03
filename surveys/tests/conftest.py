from surveys.models import Choice, Question, Survey, InvestorCategory
from profiles.models import Profile
from users.models import User
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


@pytest.fixture
def create_categories():
    categories = [
        {"name": "wealth_managements.profiles.conservative", "range_from": 1, "range_to": 7},
        {"name": "wealth_managements.profiles.medium", "range_from": 8, "range_to": 13},
        {"name": "wealth_managements.profiles.risky", "range_from": 14, "range_to": 18}
    ]
    for category in categories:
        InvestorCategory.objects.create(**category)


@pytest.fixture
def test_user():
    return User.objects.create_user('test', 'test')


@pytest.fixture
def user_profile_with_investor_score(test_user):
    def uwis(score: int):
        user_profile = Profile.objects.get(user_id=test_user.id)
        user_profile.investor_score = score
        user_profile.save()
        return user_profile

    return uwis
