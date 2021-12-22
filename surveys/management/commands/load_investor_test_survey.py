from django.core.management.base import BaseCommand
from surveys.models import Survey, Question, Choice


class Command(BaseCommand):
    help = 'Creates a survey called investor test and loads the questions with their corresponding options and scores'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing'))
        questions = [
            {
                'text': ('Estás en un programa de juegos de televisión y puedes elegir uno de los siguientes premios. '
                         '¿Cuál te llevarías?'),
                'order': 1,
                'choices': [{'text': '$ 1,000 en efectivo', 'value': 1},
                            {'text': 'Un 50% de posibilidades de ganar $ 5,000', 'value': 2},
                            {'text': 'Un 25% de posibilidades de ganar $ 10,000', 'value': 3},
                            {'text': 'Un 5% de posibilidades de ganar $ 100,000', 'value': 4}]
            },
            {
                'text': ('Cuando piensa en la palabra “riesgo”, '
                         '¿cuál de las siguientes palabras le viene a la mente primero?'),
                'order': 2,
                'choices': [{'text': 'Pérdida', 'value': 1},
                            {'text': 'Incertidumbre', 'value': 2},
                            {'text': 'Oportunidad', 'value': 3},
                            {'text': 'Emoción', 'value': 4}]
            },
            {
                'text': 'En general, ¿Cómo te describirías como tomador de riesgos?',
                'order': 3,
                'choices': [{'text': 'Una persona jugada', 'value': 4},
                            {'text': 'Soy una persona dispuesta a correr riesgos'
                                     'después de completar una investigación adecuada.', 'value': 3},
                            {'text': 'Persona cautelosa', 'value': 2},
                            {'text': 'Verdaderamente evito los riesgos ', 'value': 1}]
            },
            {
                'text': 'Si recibes inesperadamente 20,000 dólares para invertir, ¿qué harías?',
                'order': 4,
                'choices': [{'text': ('Depositarlo en una cuenta bancaria, '
                                      'una cuenta remunerada o un plazo fijo.'), 'value': 1},
                            {'text': 'Comprar Bitcoin y otras criptomonedas estables', 'value': 2},
                            {'text': 'Invertir en proyectos cripto iniciales con promesa de crecimiento ', 'value': 3}]
            },
            {
                'text': ('Ahora, con estos $ 20 000 se te presentan 3 opciones para diversificar tu inversión, '
                         '¿cuál de las siguientes opciones de inversión encontrarás más atractivo?'),
                'order': 5,
                'choices': [{'text': ('60% en inversiones de bajo riesgo 30% en inversiones '
                                      'de riesgo medio 10% en inversiones de alto riesgo '), 'value': 1},
                            {'text': ('30% en inversiones de bajo riesgo 40% en inversiones '
                                      'de medio riesgo 30% en inversiones de alto riesgo'), 'value': 2},
                            {'text': ('10% en inversiones de bajo riesgo 40% en inversiones '
                                      'de medio riesgo 50% en inversiones de alto riesgo'), 'value': 3}]
            }]

        survey = Survey.objects.create(name='investor_test')
        for question in questions:
            created_question = Question.objects.create(survey=survey, text=question['text'], order=question['order'])
            for choice in question['choices']:
                Choice.objects.create(question=created_question, text=choice['text'], value=choice['value'])

        self.stdout.write(self.style.SUCCESS('Successful data upload'))
