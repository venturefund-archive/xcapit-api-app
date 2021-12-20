from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Surveys'
        verbose_name = 'Survey'


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


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    value = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Choice'
        verbose_name = 'Choices'
