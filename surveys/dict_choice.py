from surveys.models import Choice


class DictChoice:
    def __init__(self, choice: Choice, language: str):
        self.choice = choice
        self.language = language

    def _translated_choice_text(self):
        return self.choice.translated_choices.get(language=self.language).text

    def value(self):
        return {"text": self._translated_choice_text(), "points": self.choice.value}
