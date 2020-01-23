from django.urls import path
from .views import TermsAndConditionsViewSet

app_name = 'terms_and_conditions'

urlpatterns = [
    path(
        'user/<user_id>',
        TermsAndConditionsViewSet.as_view({'post': 'create', 'get': 'retrieve'}),
        name="terms-and-conditions"
    ),
    path(
        '<pk>',
        TermsAndConditionsViewSet.as_view({'put': 'update'}),
        name="terms-and-conditions-update"
    )
]
