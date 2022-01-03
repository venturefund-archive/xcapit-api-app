import pytest
from users.models import User


@pytest.fixture
def language_mock():
    return {
        'language': 'en'
    }


@pytest.fixture
def test_user():
    return User.objects.create_user('test', 'test')
