from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import TermsAndConditionsSerializer
from .models import TermsAndConditions
from users.models import User
from rest_framework import status
from core.helpers import ResponseHelper
add_error_code = ResponseHelper.add_error_code


class TermsAndConditionsViewSet(ModelViewSet):
    serializer_class = TermsAndConditionsSerializer
    queryset = TermsAndConditions.objects.all()

    def retrieve(self, request, user_id, *args, **kwargs):
        request.user = User.objects.get(pk=user_id)
        try:
            data = TermsAndConditions.objects.get(user_id=request.user.id)
        except TermsAndConditions.DoesNotExist:
            response = Response({}, status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data)
            data = serializer.data
            response = Response(data, status=status.HTTP_200_OK)
        return response

    def create(self, request, user_id, *args, **kwargs):
        request.user = User.objects.get(pk=user_id)
        return super(TermsAndConditionsViewSet, self).create(
            request,
            *args,
            **kwargs
        )
