from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from surveys.models import Survey


class InvestorTestView(APIView):

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, name='investor_test')
        response = survey.to_json()
        return Response(response, status=200)
