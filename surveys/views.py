from surveys.dict_survey import DictSurvey
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from surveys.models import Survey, QuestionTranslation


class InvestorTestView(APIView):

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, name='investor_test')
        language = request.query_params.get('language', 'en')
        if language not in self._get_available_languages():
            language = 'en'
        response = DictSurvey(survey, language).value()
        return Response(response, status=200)

    @staticmethod
    def _get_available_languages():
        return QuestionTranslation.objects.order_by().values_list('language', flat=True).distinct()
