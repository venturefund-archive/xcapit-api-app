from surveys.models import Choice, Question, Survey, InvestorCategory, QuestionTranslation, ChoiceTranslation
from profiles.models import Profile
from users.models import User
import pytest
import json


@pytest.fixture
def create_survey():
    translated_questions = [
        {'text': 'PreguntaUno', 'language': 'es', 'question_id': 1},
        {'text': 'QuestionOne', 'language': 'en', 'question_id': 1},
        {'text': 'PreguntaDos', 'language': 'es', 'question_id': 2},
        {'text': 'QuestionTwo', 'language': 'en', 'question_id': 2},
        {'text': 'PreguntaTres', 'language': 'es', 'question_id': 3},
        {'text': 'QuestionThree', 'language': 'en', 'question_id': 3},
    ]

    translated_choices = [
        {'text': 'OpciónUno', 'language': 'es', 'value': 1},
        {'text': 'ChoiceOne', 'language': 'en', 'value': 1},
        {'text': 'OpciónDos', 'language': 'es', 'value': 2},
        {'text': 'ChoiceTwo', 'language': 'en', 'value': 2},
        {'text': 'OpciónTres', 'language': 'es', 'value': 3},
        {'text': 'ChoiceThree', 'language': 'en', 'value': 3},
    ]

    survey = Survey.objects.create(name='investor_test')

    for question_number in [0, 1, 2]:
        question = Question.objects.create(survey=survey, order=question_number)

        question_translations = [translated_question for translated_question in translated_questions if
                                 translated_question['question_id'] == question.id]

        for translation in question_translations:
            QuestionTranslation.objects.create(question=question,
                                               text=translation['text'],
                                               language=translation['language'])

        for value in [1, 2, 3]:
            choice = Choice.objects.create(question=question, value=value)

            choice_translations = [translated_choice for translated_choice in translated_choices if
                                   translated_choice['value'] == choice.value]

            for translation in choice_translations:
                ChoiceTranslation.objects.create(choice=choice,
                                                 text=translation['text'],
                                                 language=translation['language'])


@pytest.fixture
def expected_spanish_survey():
    return [
        {
            "text": "PreguntaUno",
            "order": 0,
            "options": [
                {"text": "OpciónUno", "points": 1},
                {"text": "OpciónDos", "points": 2},
                {"text": "OpciónTres", "points": 3}
            ]
        },
        {
            "text": "PreguntaDos",
            "order": 1,
            "options": [
                {"text": "OpciónUno", "points": 1},
                {"text": "OpciónDos", "points": 2},
                {"text": "OpciónTres", "points": 3}
            ]
        },
        {
            "text": "PreguntaTres",
            "order": 2,
            "options": [
                {"text": "OpciónUno", "points": 1},
                {"text": "OpciónDos", "points": 2},
                {"text": "OpciónTres", "points": 3}
            ]
        }
    ]


@pytest.fixture
def expected_english_survey():
    return [
        {
            "text": "QuestionOne",
            "order": 0,
            "options": [
                {"text": "ChoiceOne", "points": 1},
                {"text": "ChoiceTwo", "points": 2},
                {"text": "ChoiceThree", "points": 3}
            ]
        },
        {
            "text": "QuestionTwo",
            "order": 1,
            "options": [
                {"text": "ChoiceOne", "points": 1},
                {"text": "ChoiceTwo", "points": 2},
                {"text": "ChoiceThree", "points": 3}
            ]
        },
        {
            "text": "QuestionThree",
            "order": 2,
            "options": [
                {"text": "ChoiceOne", "points": 1},
                {"text": "ChoiceTwo", "points": 2},
                {"text": "ChoiceThree", "points": 3}
            ]
        }
    ]


@pytest.fixture
def expected_spanish_question_json_response():
    return {
        "text": "PreguntaUno",
        "order": 0,
        "options": [
            {"text": "OpciónUno", "points": 1},
            {"text": "OpciónDos", "points": 2},
            {"text": "OpciónTres", "points": 3}
        ]
    }


@pytest.fixture
def expected_english_question_json_response():
    return {
        "text": "QuestionOne",
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
