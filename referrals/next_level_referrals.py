import pandas as pd
from typing import List
from django.db import connection
from functools import lru_cache as cache


class NextLevelReferrals:
    def __init__(self, referrals_id: List[str]):
        self._referrals_id = referrals_id

    def _multiple_referrals(self):
        return len(self._referrals_id) > 1

    def _in_param(self):
        return f'in {tuple(self._referrals_id)}' if self._multiple_referrals() else f"='{self._referrals_id[0]}'"

    @cache
    def all(self):
        return pd.read_sql(
            'SELECT '
            'u.referral_id AS referred_id, '
            'u.id AS user_id, '
            'r.referral_id, '
            '(SELECT COUNT(w.id) > 0 FROM wallets_wallet w WHERE w.user_id=u.id) AS wallet_created '
            'FROM referrals_referral r '
            'INNER join users_user u ON u.email = r.email '
            f'WHERE r.accepted = true AND r.referral_id {self._in_param()}',
            con=connection,
            index_col='user_id'
        ).astype({'wallet_created': bool})

