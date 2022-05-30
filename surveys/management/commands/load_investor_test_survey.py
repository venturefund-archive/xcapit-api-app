import os

from django.core.management.base import BaseCommand
from surveys.models import Survey, Question, Choice, QuestionTranslation, ChoiceTranslation
import json


class Command(BaseCommand):
    help = 'Creates a survey called investor test and loads the questions with their corresponding options and scores'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing'))

        json_data = open(os.path.abspath(os.path.dirname(__file__)) + '/fixture/survey.json')
        survey_data = json.load(json_data)['survey']

        survey = Survey.objects.create(name=survey_data['name'])
        for question in survey_data['questions']:
            created_question = Question.objects.create(survey=survey, order=question['order'])
            for language in question['text']:
                QuestionTranslation.objects.create(question=created_question, language=language,
                                                   text=question['text'][language])

            for choice in question['choices']:
                created_choice = Choice.objects.create(question=created_question, value=choice['value'])
                for language in choice['text']:
                    ChoiceTranslation.objects.create(choice=created_choice, language=language,
                                                     text=choice['text'][language])

        self.stdout.write(self.style.SUCCESS('Successful data upload'))
