from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.helpers import ResponseHelper
from .models import Profile
from .serializers import ProfileSerializer, PersonalDataSerializer, BillDataSerializer, ProfileSerializerFactory
from .services import ProfileUpdateService

add_error_code = ResponseHelper.add_error_code


class ProfileAPIView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request, user_id):
        try:
            profile = Profile.objects.select_related('user').get(user_id=user_id)
        except Profile.DoesNotExist:
            profile = None
        if profile is not None:
            serializer = self.serializer_class(profile)
            response = Response(serializer.data, status.HTTP_200_OK)
        else:
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            response = add_error_code(response, 'profiles.retrieve.doesNotExists')
        return response

    def put(self, request, user_id):
        profiles = Profile.objects.select_related('user').filter(user_id=user_id)
        if not profiles.exists():
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'profiles.update.doesNotExists')
        profile = profiles.last()
        profile_update_service = ProfileUpdateService(self.serializer_class, profile, request.data)
        updated = profile_update_service.update()

        if not updated:
            response = Response(profile_update_service.errors, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'profiles.update.invalidData')

        return Response(True, status.HTTP_200_OK)


class ProfileValidAPIView(APIView):
    serializer_class = ProfileSerializer
    profile_serializer_factory = ProfileSerializerFactory

    def get(self, request, user_id):
        """ Check if user's profile is valid
        
        Parameters
        ----------

        user_id : int
            User id
        
        Returns
        -------
        dict
            Profile valid:
            {
                valid: bool
            }
        """
        validation_type = request.query_params.get('validation_type', None)
        profiles = Profile.objects.select_related('user').filter(user_id=user_id)
        if not profiles.exists():
            return Response({}, status.HTTP_204_NO_CONTENT)
        profile = profiles.last()
        serialized_profile = self.serializer_class(profile)
        serializer = self.profile_serializer_factory.create(validation_type, data=serialized_profile.data)
        valid = serializer.is_valid(raise_exception=False)
        response = Response({'valid': valid}, status.HTTP_200_OK)
        return response


class PersonalDataAPIView(APIView):
    serializer_class = PersonalDataSerializer

    def put(self, request, user_id):
        profiles = Profile.objects.select_related('user').filter(user_id=user_id)
        if not profiles.exists():
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'profiles.update.doesNotExists')
        profile = profiles.last()
        profile_update_service = ProfileUpdateService(self.serializer_class, profile, request.data)
        updated = profile_update_service.update()

        if not updated:
            response = Response(profile_update_service.errors, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'profiles.update.invalidData')

        return Response(True, status.HTTP_200_OK)


class BillDataAPIView(APIView):
    serializer_class = BillDataSerializer

    def put(self, request, user_id):
        profiles = Profile.objects.select_related('user').filter(user_id=user_id)
        if not profiles.exists():
            response = Response({}, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'profiles.update.doesNotExists')
        profile = profiles.last()
        profile_update_service = ProfileUpdateService(self.serializer_class, profile, request.data)
        updated = profile_update_service.update()

        if not updated:
            response = Response(profile_update_service.errors, status.HTTP_400_BAD_REQUEST)
            return add_error_code(response, 'profiles.update.invalidData')

        return Response(True, status.HTTP_200_OK)

