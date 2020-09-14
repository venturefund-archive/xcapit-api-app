from django.urls import path
from .views import UserViewSet

app_name = 'administration'

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<pk>', UserViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'}), name='users'),
]
