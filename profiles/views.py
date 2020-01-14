from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.helpers import ResponseHelper
from .models import Profile
from .serializers import ProfileSerializer
add_error_code = ResponseHelper.add_error_code


class ProfileAPIView(APIView):

    serializer_class = ProfileSerializer

    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            profile = Profile.objects.select_related('user').get(
                user_id=user_id)
        except Profile.DoesNotExist:
            profile = None
        if profile is not None:
            serializer = self.serializer_class(profile)
            response = Response(serializer.data, status.HTTP_200_OK)
        else:
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            response = add_error_code(response,
                                      'profiles.retrieve.doesNotExists')
        return response

    def put(self, request):
        user_id = request.query_params.get('user_id')
        try:
            profile = Profile.objects.select_related('user').get(
                user_id=user_id)
        except Profile.DoesNotExist:
            profile = None
        if profile is not None:
            serializer = self.serializer_class(
                instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = Response(True, status.HTTP_200_OK)
            else:
                response = Response({}, status.HTTP_400_BAD_REQUEST)
                response = add_error_code(response,
                                          'profiles.update.invalidData')
        else:
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            response = add_error_code(response,
                                      'profiles.update.doesNotExists')
        return response
