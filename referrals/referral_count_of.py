from referrals.next_level_referrals import NextLevelReferrals


class ReferralCountOf():
    def __init__(self, referrals: NextLevelReferrals, wallet: bool):
        self._referrals = referrals
        self._wallet = wallet

    def value(self):
        return len(self._referrals.all()[self._referrals.all()['wallet_created'] == self._wallet])
