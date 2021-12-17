from django.core.exceptions import ValidationError
from django.db import models
import json


class Survey(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Surveys'
        verbose_name = 'Survey'

    def to_json(self):
        questions = self.questions.all()
        return json.dumps([question.to_dict() for question in questions])


def _question_order_value():
    number = Question.objects.order_by('-order').first()
    return number.order + 1 if number else 0


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    order = models.IntegerField(default=_question_order_value)
    text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('survey', 'order')
        ordering = ['order']
        verbose_name_plural = 'Questions'
        verbose_name = 'Question'

    def to_dict(self):
        return {"text": self.text,
                "order": self.order,
                "options": [choice.to_dict() for choice in self.choices.all()]}


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    value = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Choice'
        verbose_name = 'Choices'

    def to_dict(self):
        return {"text": self.text, "points": self.value}
