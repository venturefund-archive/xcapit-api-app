import pytest
from unittest.mock import Mock
from users.serializer import CustomTokenObtainPairSerializer


def test_custom_token_obtain_pair_serializer_create():
    assert CustomTokenObtainPairSerializer().create(Mock()) is None


def test_custom_token_obtain_pair_serializer_update():
    assert CustomTokenObtainPairSerializer().update(Mock(), Mock()) is None
