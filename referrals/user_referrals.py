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
        return NextLevelReferrals(self.first_order().all().referred_id)

    def to_dict(self):
        return {"first_order": {"with_wallet": ReferralCountOf(self.first_order(), True).value(),
                                "without_wallet": ReferralCountOf(self.first_order(), False).value(),
                                "reward": FIRST_ORDER_REWARD},
                "second_order": {"with_wallet": ReferralCountOf(self.second_order(), True).value(),
                                 "without_wallet": ReferralCountOf(self.second_order(), False).value(),
                                 "reward": SECOND_ORDER_REWARD}
                }
