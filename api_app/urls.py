"""api_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('v1/api/users/', include('users.urls', namespace='users')),
    path('v1/api/stats/', include('stats.urls', namespace='stats')),
    path('v1/api/profiles/', include('profiles.urls', namespace='profiles')),
    path('v1/api/referrals/', include('referrals.urls', namespace='referrals')),
    path('v1/api/terms_and_conditions/', include('terms_and_conditions.urls', namespace='terms_and_conditions')),
    path('v1/api/administration/', include('administration.urls', namespace='administration')),
    path('v1/api/subscription_plans/', include('subscription_plans.urls', namespace='subscription_plans')),
    path('v1/api/wallets/', include('wallets.urls', namespace='wallets')),
    path('v1/api/surveys/', include('surveys.urls', namespace='surveys')),
    path('v1/api/admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
]
