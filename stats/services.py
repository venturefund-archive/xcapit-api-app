
from .models import Logs, LoginHistory
from users.models import User


class StatsService:

    def get_fund_summary_views(self, user_id=None):
        res = Logs.objects.filter(component_id='FundSummaryPage')
        if user_id:
            res = res.filter(user_id=user_id)
        return res.count()

    def get_fund_balance_views(self, user_id=None):
        res = Logs.objects.filter(component_id='FundBalancePage')
        if user_id:
            res = res.filter(user_id=user_id)
        return res.count()

    def get_login_count(self, user_id=None):
        success = LoginHistory.objects.filter(logged=True)
        failed = LoginHistory.objects.filter(logged=False)
        if user_id:
            user = User.objects.get(pk=user_id)
            success = success.filter(email=user.email)
            failed = failed.filter(email=user.email)
        return {'success': success.count(), 'failed': failed.count()}

    def get_open_count(self, user_id=None):
        res = Logs.objects.filter(event_id='load')
        if user_id:
            res = res.filter(user_id=user_id)
        return res.count()

    def get_fund_actions_count(self, user_id=None):
        pause_fund = Logs.objects.filter(button_id='Pause Fund',
                                         event_id='click')
        resume_fund = Logs.objects.filter(button_id='Resume Fund',
                                          event_id='click')
        finalize_fund = Logs.objects.filter(button_id='Finalize Fund',
                                            event_id='click')
        renew_fund = Logs.objects.filter(button_id='Renew Fund',
                                         event_id='click')

        if user_id:
            pause_fund = pause_fund.filter(user_id=user_id)
            resume_fund = resume_fund.filter(user_id=user_id)
            finalize_fund = finalize_fund.filter(user_id=user_id)
            renew_fund = renew_fund.filter(user_id=user_id)

        actions = {
            'pause_fund': pause_fund.count(),
            'resume_fund': resume_fund.count(),
            'finalize_fund': finalize_fund.count(),
            'renew_fund': renew_fund.count()
        }
        return actions
