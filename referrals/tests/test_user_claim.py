import pytest
from referrals.user_claim import UserClaim
from users.models import User
from unittest.mock import Mock
from referrals.models import Campaign, ClaimStatus


@pytest.mark.django_db
def test_user_claim():
    assert UserClaim(Mock(spec=User), Mock(spec=Campaign))


@pytest.mark.django_db
def test_user_claim_last_status_without_claim(user_mock, campaign_mock):
    user_claim = UserClaim(user_mock, campaign_mock)
    assert user_claim.last_status().count() == 0


@pytest.mark.django_db
def test_user_claim_last_status_empty(user_mock, campaign_mock, claim_mock):
    user_claim = UserClaim(user_mock, campaign_mock)
    assert user_claim.last_status().count() == 0


@pytest.mark.django_db
def test_user_claim_last_status_not_empty(user_mock, campaign_mock, claim_mock):
    ClaimStatus.objects.create(status='claimed', claim=claim_mock)
    ClaimStatus.objects.create(status='delivered', claim=claim_mock)
    user_claim = UserClaim(user_mock, campaign_mock)
    assert user_claim.last_status().count() == 1

