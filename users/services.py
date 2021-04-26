import random
from hashids import Hashids
from .models import User
from .emails import EmailValidation
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.response import Response
from rest_framework import status


def get_hashid(id, min_length=6, alphabet='abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'):
    hashids = Hashids(min_length=min_length, alphabet=alphabet)
    return hashids.encode(int(id), random.randint(0, 73))


class ResendEmailValidationService:

    def __init__(self, data):
        self._send_email_validation_class = EmailValidation()
        self._user = None
        self._uidb64 = data.get('uidb64', None)
        self._email = data.get('email', None)
        self._response = None

    def execute(self):
        self._decode_uidb64()
        self._get_user()
        self._check_if_user_is_none()
        return self._response

    def _get_user(self):
        filter_kwargs = self.get_filter_parameter()
        try:
            self._user = User.objects.get(**filter_kwargs)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            self._user = None

    def get_filter_parameter(self):
        filter_kwargs = {'pk': self._uidb64} if self._uidb64 is not None else {'email': self._email}
        return filter_kwargs

    def _decode_uidb64(self):
        if self._uidb64 is not None:
            self._uidb64 = force_str(urlsafe_base64_decode(self._uidb64))

    def _check_if_user_is_none(self):
        if self._user is not None:
            self._is_active()
        else:
            self._response = Response({'error_code': 'users.sendEmailValidationToken.user'},
                                      status.HTTP_400_BAD_REQUEST)

    def _is_active(self):
        if self._user.is_active:
            self._response = Response({'error_code': 'users.sendEmailValidationToken.userAlreadyActive'},
                                      status.HTTP_400_BAD_REQUEST)
        else:
            self._send_email()

    def _send_email(self):
        self._send_email_validation_class.send(self._user)
        self._response = Response({}, status.HTTP_200_OK)
