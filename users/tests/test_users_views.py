import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status


@pytest.mark.wip
@pytest.mark.django_db
@pytest.mark.parametrize('email, user_is_active, expected_status, expected_response', [
    ['test@test.com', False, status.HTTP_200_OK, {}],
    ['test@test.com', True, status.HTTP_400_BAD_REQUEST,
     {'error_code': 'users.sendEmailValidationToken.userAlreadyActive'}],
    ['testqwd@test.com', False, status.HTTP_400_BAD_REQUEST, {'error_code': 'users.sendEmailValidationToken.user'}]])
@patch('users.emails.EmailValidation.notifications_client.send_email_validation')
def test_send_email_validation_token(mock_send_email, client, create_user, email, user_is_active, expected_status,
                                     expected_response):
    mock_send_email.status_code = 200
    create_user(email='test@test.com', password="test", is_active=user_is_active)
    response = client.post(
        reverse('users:send-email-validation'),
        data={"email": email},
        content_type='application/json'
    )
    assert response.status_code == expected_status
    assert response.json() == expected_response
