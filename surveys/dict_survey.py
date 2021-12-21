from surveys.dict_question import DictQuestion
from surveys.models import Survey
import json


class DictSurvey:
    def __init__(self, survey: Survey):
        self.survey = survey

    def value(self):
        return [DictQuestion(question).value() for question in self.survey.questions.all()]
