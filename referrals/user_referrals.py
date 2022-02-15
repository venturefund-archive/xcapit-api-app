from api_app.settings import NEW_CAMPAIGN, OLD_CAMPAIGN
from core.datetime.datetime_of import DefaultDatetimeOf
from core.datetime.datetime_range import DatetimeRange
from core.datetime.utc_datetime_of import UTCDatetimeOf
from referrals.filtered_referral_count import FilteredReferralCount
from functools import lru_cache as cache
from referrals.referral_count_of import ReferralCountOf
from referrals.next_level_referrals import NextLevelReferrals

FIRST_ORDER_REWARD = 1
SECOND_ORDER_REWARD = 0.5


class UserReferrals:
    def __init__(self, first_order: NextLevelReferrals = None, second_order: NextLevelReferrals = None):
        self._second_order = second_order
        self._first_order = first_order

    @cache
    def first_order(self):
        return self._first_order

    @cache
    def second_order(self):
        return self._second_order

    def to_dict(self):
        return {
            'first_order': {
                'with_wallet': self._order_count_since(self.first_order(), True, NEW_CAMPAIGN).value(),
                'without_wallet': self._order_count_to(self.first_order(), False, OLD_CAMPAIGN).value() +
                                  self._order_count_to(self.first_order(), True, OLD_CAMPAIGN).value(),
                'reward': FIRST_ORDER_REWARD
            },
            'second_order': {
                'with_wallet': 0,
                'without_wallet': self._order_count_to(self.second_order(), False, OLD_CAMPAIGN).value(),
                'reward': SECOND_ORDER_REWARD
            }
        }

    @staticmethod
    def _order_count_since(order: NextLevelReferrals, with_wallet: bool, a_campaign_datetime: str) -> FilteredReferralCount:
        return FilteredReferralCount(
            ReferralCountOf(order, with_wallet),
            DatetimeRange(since=UTCDatetimeOf(DefaultDatetimeOf(a_campaign_datetime))))

    @staticmethod
    def _order_count_to(order: NextLevelReferrals, with_wallet: bool, a_campaign_datetime: str) -> FilteredReferralCount:
        return FilteredReferralCount(
            ReferralCountOf(order, with_wallet),
            DatetimeRange(to=UTCDatetimeOf(DefaultDatetimeOf(a_campaign_datetime))))
