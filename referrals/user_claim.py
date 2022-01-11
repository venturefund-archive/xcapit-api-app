from users.models import User
from django.db.models import QuerySet
from referrals.models import Campaign, ClaimStatus, Claim


class LastStatusResponse:
    def __init__(self, last_status: QuerySet):
        self._last_status = last_status

    def to_dict(self) -> dict:
        return self._last_status.values('status', 'date')[0] if self.count() else {}

    def count(self):
        return self._last_status.count()


class UserClaim:
    def __init__(self, user: User, campaign: Campaign):
        self._user = user
        self._campaign = campaign

    def last_status(self) -> LastStatusResponse:
        claims = Claim.objects.filter(user=self._user, campaign=self._campaign)
        return LastStatusResponse(
            claims.last().claim_statuses.order_by('-date')[:1] if claims.exists() else ClaimStatus.objects.none()
        )
