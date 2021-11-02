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
        # Filtrar por accepted = True
        return pd.read_sql(
            'select '
            'u.referral_id as referred_id, '
            'u.id as user_id, '
            'r.referral_id, '
            '(select count(w.id) > 0 from wallets_wallet w where w.user_id=u.id) as wallet_created '
            'from referrals_referral r '
            'inner join users_user u on u.email = r.email '
            f'where r.referral_id {self._in_param()}',
            con=connection,
            index_col='user_id'
        ).astype({'wallet_created': bool})
