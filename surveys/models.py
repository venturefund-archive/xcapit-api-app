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

    class Meta:
        unique_together = ('survey', 'order')
        ordering = ['order']
        verbose_name_plural = 'Questions'
        verbose_name = 'Question'


class QuestionTranslation(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='translated_questions')
    text = models.CharField(max_length=200)
    language = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = 'translated_questions'
        verbose_name = 'translated_question'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    value = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Choice'
        verbose_name = 'Choices'


class ChoiceTranslation(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='translated_choices')
    text = models.CharField(max_length=200)
    language = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = 'translated_choices'
        verbose_name = 'translated_choice'


class InvestorCategory(models.Model):
    name = models.CharField(max_length=60)
    range_from = models.IntegerField()
    range_to = models.IntegerField()
