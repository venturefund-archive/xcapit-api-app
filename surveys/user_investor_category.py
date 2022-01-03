from profiles.models import Profile
from surveys.models import InvestorCategory


class UserInvestorCategory:
    def __init__(self, user_profile: Profile):
        self._user_profile = user_profile

    def value(self):
        investor_category = InvestorCategory.objects.filter(range_from__lte=self._user_profile.investor_score,
                                                            range_to__gte=self._user_profile.investor_score)
        return investor_category[0].name if investor_category else 'wealth_managements.profiles.no_category'
