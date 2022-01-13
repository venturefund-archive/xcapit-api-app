from surveys.dict_choice import DictChoice
from surveys.models import Question


class DictQuestion:
    def __init__(self, question: Question):
        self.question = question

    def value(self):
        return {"text": self.question.text,
                "order": self.question.order,
                "options": [DictChoice(choice).value() for choice in self.question.choices.all()]}
