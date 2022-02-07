from core.datetime.datetime_range import DatetimeRange
from referrals.next_level_referrals import NextLevelReferrals


# TODO: may be a FilteredReferrals object will has the filtering logic 🤔
# FilterdedReferrals(ReferralCountOf, DatetimeRange).value() 🤔
class ReferralCountOf:
    def __init__(self, referrals: NextLevelReferrals, wallet: bool, a_datetime_range: DatetimeRange = DatetimeRange()):
        self._a_datetime_range = a_datetime_range
        self._referrals = referrals
        self._wallet = wallet

    def value(self):
        all_ = self._referrals.all()[self._referrals.all()['wallet_created'] == self._wallet]
        # TODO: should I create a StringOf with since().value()/to().value()
        all_ = all_[all_['created_at'] >= self._a_datetime_range.since().value()] if self._a_datetime_range.since() else all_
        all_ = all_[all_['created_at'] <= self._a_datetime_range.to().value()] if self._a_datetime_range.to() else all_
        return len(all_)
