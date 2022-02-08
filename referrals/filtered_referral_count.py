from core.datetime.datetime_range import DatetimeRange
from core.value import Value
from referrals.referral_count_of import ReferralCountOf


class FilteredReferralCount(Value):

    def __init__(self, referral_count: ReferralCountOf, a_datetime_range: DatetimeRange = DatetimeRange()):
        self._a_datetime_range = a_datetime_range
        self._referral_count = referral_count

    def value(self) -> int:
        all_ = self._referral_count.raw_df()
        all_ = all_[all_['created_at'] >= self._a_datetime_range.since().value()] if self._a_datetime_range.since() else all_
        all_ = all_[all_['created_at'] <= self._a_datetime_range.to().value()] if self._a_datetime_range.to() else all_
        return len(all_)
