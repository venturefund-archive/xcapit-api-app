import pytest
from users.models import User


@pytest.fixture
def create_user():
    def cu(email, password, is_superuser=False, is_active=True):
        user = User.objects.create_user(**{
            'email': email,
            'password': password
        })
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.save()
    return cu
