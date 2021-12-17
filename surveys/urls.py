from django.urls import path
from surveys.views import InvestorTestView

app_name = 'surveys'

urlpatterns = [
    path('investor_test', InvestorTestView.as_view(), name='investor-test'),
]
