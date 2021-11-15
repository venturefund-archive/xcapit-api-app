import pytest
from datetime import datetime
from wallets.models import NFTRequest
from django.db import IntegrityError


@pytest.mark.django_db
def test_nft_request_model(user_mock):
    nft_request = NFTRequest.objects.create(user=user_mock)
    assert nft_request.user == user_mock
    assert nft_request.status == 'claimed'
    assert nft_request.claimed_at.date() == datetime.now().date()


@pytest.mark.django_db
def test_wallet_model_unique(user_mock):
    with pytest.raises(IntegrityError) as e:
        NFTRequest.objects.create(user=user_mock)
        NFTRequest.objects.create(user=user_mock)
        assert e
