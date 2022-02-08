from api_app.settings import NEW_CAMPAIGN, OLD_CAMPAIGN
from core.datetime.datetime_of import DatetimeOf
from core.datetime.datetime_range import DatetimeRange
from referrals.filtered_referral_count import FilteredReferralCount
from users.models import User
from functools import lru_cache as cache
from referrals.referral_count_of import ReferralCountOf
from referrals.next_level_referrals import NextLevelReferrals

FIRST_ORDER_REWARD = 1
SECOND_ORDER_REWARD = 0.5


class UserReferrals:
    def __init__(self, user: User):
        self._user = user

    @cache
    def first_order(self):
        return NextLevelReferrals([self._user.referral_id])

    @cache
    def second_order(self):
        return NextLevelReferrals(list(self.first_order().all().referred_id))

    def to_dict(self):
        return {
            'first_order': {
                'with_wallet': self._order_count(self.first_order(), True, NEW_CAMPAIGN).value(),
                'without_wallet': self._order_count(self.first_order(), False, OLD_CAMPAIGN).value() +
                                  self._order_count(self.first_order(), True, OLD_CAMPAIGN).value(),
                'reward': FIRST_ORDER_REWARD
            },
            'second_order': {
                'with_wallet': 0,
                'without_wallet': self._order_count(self.second_order(), False, OLD_CAMPAIGN).value(),
                'reward': SECOND_ORDER_REWARD
            }
        }

    @staticmethod
    def _order_count(order: NextLevelReferrals, with_wallet: bool, a_campaign_datetime: str) -> FilteredReferralCount:
        return FilteredReferralCount(
            ReferralCountOf(order, with_wallet),
            DatetimeRange(since=DatetimeOf(a_campaign_datetime)))
