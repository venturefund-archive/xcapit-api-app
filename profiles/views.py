from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.helpers import ResponseHelper
from .models import Profile
from .serializers import ProfileSerializer, ProfileValidSerializer
add_error_code = ResponseHelper.add_error_code


class ProfileAPIView(APIView):

    serializer_class = ProfileSerializer

    def get(self, request, user_id):
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

    def put(self, request, user_id):
        try:
            profile = Profile.objects.select_related('user').get(
                user_id=user_id
            )
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


class ProfileValidAPIView(APIView):
    serializer_class = ProfileValidSerializer

    def get(self, request, user_id):
        """Retorna si el perfil del usuario del id recibido es valido
        
        Parameters
        ----------

        user_id : int
            Id del usuario
        
        Returns
        -------
        dict
            Profile valido o invalido de la siguiente forma:
            {
                valid: bool
            }
        """        
        try:
            profile = Profile.objects.select_related('user').get(
                user_id=user_id)
        except Profile.DoesNotExist:
            profile = None

        if profile is not None:
            serialized_profile = self.serializer_class(profile)
            serializer = self.serializer_class(data=serialized_profile.data)
            valid = serializer.is_valid(raise_exception=False)
            response = Response({'valid': valid }, status.HTTP_200_OK)
        else:
            response = Response({}, status.HTTP_204_NO_CONTENT)
        return response
