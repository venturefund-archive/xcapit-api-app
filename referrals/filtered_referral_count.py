import pandas
from core.datetime.datetime_range import DatetimeRange
from core.value import Value
from referrals.referral_count_of import ReferralCountOf


class FilteredReferralCount(Value):

    def __init__(self, referral_count: ReferralCountOf, a_datetime_range: DatetimeRange = DatetimeRange()):
        self._a_datetime_range = a_datetime_range
        self._referral_count = referral_count

    def value(self) -> int:
        referral_count_df = self._referral_count.raw_df()
        referral_count_df = self._filter_by_since(referral_count_df)
        referral_count_df = self._filter_by_to(referral_count_df)
        return len(referral_count_df)

    def _filter_by_to(self, referral_count_df: pandas.DataFrame):
        return referral_count_df[self._to_condition(referral_count_df)] \
            if self._a_datetime_range.to() else referral_count_df

    def _filter_by_since(self, referral_count_df: pandas.DataFrame):
        return referral_count_df[self._since_condition(referral_count_df)] \
            if self._a_datetime_range.since() else referral_count_df

    def _since_condition(self, referral_count_df: pandas.DataFrame):
        return referral_count_df['created_at'] >= self._a_datetime_range.since().value()

    def _to_condition(self, referral_count_df: pandas.DataFrame):
        return referral_count_df['created_at'] <= self._a_datetime_range.to().value()
