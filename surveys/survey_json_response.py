from surveys.dict_question import DictQuestion
from surveys.models import Survey
import json


class SurveyJsonResponse:
    def __init__(self, survey: Survey):
        self.survey = survey

    def value(self):
        return json.dumps([DictQuestion(question).value() for question in self.survey.questions.all()])
