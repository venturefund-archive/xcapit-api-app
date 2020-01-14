from users.models import User
from django.urls import reverse
import json


user_test_data = {
    'email': 'test1@test.com',
    'password': 'test'
}


def get_credentials(client, email='', password='', new_user=True, is_superuser=False):
    email = email if email else user_test_data.get('email')
    password = password if password else user_test_data.get('password')
    if new_user:
        create_user(email, password, is_superuser)
    payload = json.dumps({
        'email': email,
        'password': password
    })
    credentials = client.post(
        reverse('users:user-login'), data=payload,
        content_type='application/json').data
    return {'HTTP_AUTHORIZATION': f'Bearer {credentials.get("access")}'}


def create_user(email, password, is_superuser):
    user = User.objects.create_user(**{
        'email': email,
        'password': password
    })
    user.is_active = True
    user.is_superuser = is_superuser
    user.save()
    return user
