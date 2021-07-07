import pytest
from users import test_utils


@pytest.fixture
def create_user():
    def cu(email='maxi@maxi.com', password='1234Qwerty', is_superuser=False):
        return test_utils.create_user(email, password, is_superuser)
    return cu
