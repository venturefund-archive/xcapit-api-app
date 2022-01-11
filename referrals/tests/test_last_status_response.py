from datetime import datetime

import pytest
from unittest.mock import Mock
from django.db.models import QuerySet

from referrals.models import ClaimStatus
from referrals.user_claim import LastStatusResponse


def test_last_status_response_count():
    assert LastStatusResponse(Mock(count=lambda: 1, spec=QuerySet)).count() == 1


def test_last_status_response_to_dict_empty():
    assert LastStatusResponse(Mock(count=lambda: 0, spec=QuerySet)).to_dict() == {}


@pytest.mark.django_db
def test_last_status_response_to_dict(claim_mock):
    ClaimStatus.objects.create(status='claimed', claim=claim_mock, date=datetime(2021, 10, 1))
    last_status_response = LastStatusResponse(ClaimStatus.objects.filter(claim=claim_mock))
    assert last_status_response.to_dict()['status'] == 'claimed'
