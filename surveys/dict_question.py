from surveys.dict_choice import DictChoice
from surveys.models import Question


class DictQuestion:
    def __init__(self, question: Question, language: str):
        self.question = question
        self.language = language

    def _translated_question_text(self):
        return self.question.translated_questions.get(language=self.language).text

    def value(self):
        return {"text": self._translated_question_text(),
                "order": self.question.order,
                "options": [DictChoice(choice, self.language).value() for choice in self.question.choices.all()]}
