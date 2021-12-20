from surveys.models import Choice


class DictChoice:
    def __init__(self, choice: Choice):
        self.choice = choice

    def value(self):
        return {"text": self.choice.text, "points": self.choice.value}
