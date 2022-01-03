import pytest
from io import StringIO
from surveys.models import InvestorCategory
from django.core.management import call_command


@pytest.mark.django_db
def test_command_load_investor_categories():
    out = StringIO()
    call_command('load_investor_categories', stdout=out)
    assert 'Successful data upload' in out.getvalue()
    assert InvestorCategory.objects.all().count() == 3
    conservative = InvestorCategory.objects.get(name="wealth_managements.profiles.conservative")
    assert conservative.range_from == 1 and conservative.range_to == 7
    medium = InvestorCategory.objects.get(name="wealth_managements.profiles.medium")
    assert medium.range_from == 8 and medium.range_to == 13
    risky = InvestorCategory.objects.get(name="wealth_managements.profiles.risky")
    assert risky.range_from == 14 and risky.range_to == 18
