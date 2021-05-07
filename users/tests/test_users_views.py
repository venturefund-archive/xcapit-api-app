import pytest
from django.urls import reverse
from unittest.mock import patch, Mock
from rest_framework import status
from users.models import User


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


USER_DATA = {
     'iss': 'https://accounts.google.com',
     'sub': '110169484474386276334',
     'azp': '840751586681-35nflvl2e8e8tn0mb6uin9bgrptjgkf6.apps.googleusercontent.com',
     'aud': '840751586681-35nflvl2e8e8tn0mb6uin9bgrptjgkf6.apps.googleusercontent.com',
     'iat': '1433978353',
     'exp': '1433981953',
     'email': 'testuser@gmail.com',
     'email_verified': True,
     'name' : 'Test User',
     'picture': 'https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg',
     'given_name': 'Test',
     'family_name': 'User',
     'locale': 'en'
}

USER_DATA_FALSE = {
     'aud': 'abc123',
     'email': 'testuser@gmail.com',
     'email_verified': True,
}

USER_DATA_FALSE_2 = {
     'aud': '840751586681-35nflvl2e8e8tn0mb6uin9bgrptjgkf6.apps.googleusercontent.com',
     'email': 'testuser@gmail.com',
     'email_verified': False,
}


@pytest.mark.django_db
@pytest.mark.parametrize('user_exist, user_password, result', [
    [False, '', ''],
    [True, '', ''],
    [True, 'asd123', {'error': 'User register with another account', 'error_code': 'users.login.notGoogleLoginUser'}]
])
@patch('users.views.LoginWithGoogleAPIView.verify_google_oauth2')
def test_login_with_google_new_user(mock_google_response, client, user_exist, user_password, result):
    if user_exist is True:
        user = User(email="testuser@gmail.com", password=user_password, is_active=True)
        user.save()

    mock_google_response.return_value = USER_DATA
    data = {'id_token': 'TestToken'}

    response = client.post(reverse('users:google-user-login'),
        data=data,
        content_type='application/json')

    assert response

    if len(user_password) > 0:
        assert response.json() == result


@pytest.mark.django_db
@pytest.mark.parametrize('google_response, result', [
    [USER_DATA_FALSE, {'error': 'Error client access', 'error_code': 'users.login.notClientAccess'}],
    [USER_DATA_FALSE_2, {'error': 'Google account not verified', 'error_code': 'users.login.notVerifiedGoogleAccount'}]
])
@patch('users.views.LoginWithGoogleAPIView.verify_google_oauth2')
def test_login_with_google_exceptions(mock_google_response, client, google_response, result):
    user = User(email="testuser@gmail.com", password="asdf123", is_active=True)
    user.save()
    mock_google_response.return_value = google_response
    data = {'id_token': 'TestToken'}

    response = client.post(reverse('users:google-user-login'),
        data=data,
        content_type='application/json')

    assert response
    assert response.json() == result





