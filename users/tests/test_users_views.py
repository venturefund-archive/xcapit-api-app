import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize('user_is_active, data, expected_status, expected_response', [
    [False, {'uidb64': 'MQ'}, status.HTTP_200_OK, {}],
    [True, {'uidb64': 'MQ'}, status.HTTP_400_BAD_REQUEST,
     {'error_code': 'users.sendEmailValidationToken.userAlreadyActive'}],
    [False, {'uidb64': 'XXX'}, status.HTTP_400_BAD_REQUEST,
     {'error_code': 'users.sendEmailValidationToken.user'}],
    [False, {'email': 'test@test.com'}, status.HTTP_200_OK, {}],
    [True, {'email': 'test@test.com'}, status.HTTP_400_BAD_REQUEST,
     {'error_code': 'users.sendEmailValidationToken.userAlreadyActive'}],
    [False, {'email': 'testqwd@test.com'}, status.HTTP_400_BAD_REQUEST,
     {'error_code': 'users.sendEmailValidationToken.user'}],
    [False, {}, status.HTTP_400_BAD_REQUEST,
     {'non_field_errors': ['Debe existir al menos uno de los campos requeridos: email, uidb64']}],
    [False, {'email': 'test@test.com', 'uidb64': 'MQ'}, status.HTTP_400_BAD_REQUEST,
     {'non_field_errors': ['Los campos son mutuamente exclusivos']}]])
@patch('users.emails.EmailValidation.notifications_client.send_email_validation')
def test_send_email_validation_token(mock_send_email, client, create_user, user_is_active, data, expected_status,
                                     expected_response):
    mock_send_email.status_code = 200
    create_user(email='test@test.com', password="test", is_active=user_is_active)
    response = client.post(
        reverse('users:send-email-validation'),
        data=data,
        content_type='application/json'
    )
    assert response.status_code == expected_status
    assert response.json() == expected_response
