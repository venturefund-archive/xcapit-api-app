from django.urls import path
from .views import ProfileAPIView, ProfileValidAPIView, BillDataAPIView, PersonalDataAPIView, LanguageView

app_name = 'profiles'

urlpatterns = [
    path('user/<user_id>', ProfileAPIView.as_view(), name='retrieve-update-user-profile'),
    path('user/<user_id>/bill_data', BillDataAPIView.as_view(), name='user-profile-bill-data'),
    path('user/<user_id>/personal_data', PersonalDataAPIView.as_view(), name='user-profile-personal-data'),
    path('user/<user_id>/valid', ProfileValidAPIView.as_view(), name='valid'),
    path('user/<user_id>/language/', LanguageView.as_view(), name='language'),
]
