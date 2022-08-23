from surveys.dict_question import DictQuestion
from surveys.models import Survey
import json


class DictSurvey:
    def __init__(self, survey: Survey, language: str):
        self.survey = survey
        self.language = language

    def value(self):
        return [DictQuestion(question, self.language).value() for question in self.survey.questions.all()]
