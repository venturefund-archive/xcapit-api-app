import pytest
from users.models import User


@pytest.fixture
def user_mock():
    return User.objects.create_user(email='test', password='TestPass123')
