from surveys.survey_json_response import SurveyJsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from surveys.models import Survey


class InvestorTestView(APIView):

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, name='investor_test')
        response = SurveyJsonResponse(survey).value()
        return Response(response, status=200)
