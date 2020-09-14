from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_login_failed
from profiles.models import Profile
from stats.models import LoginHistory
from .models import User
from core.helpers import RequestInfoHelper


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kargs):

    if instance and created:
        instance.profile = Profile.objects.create(user=instance)


@receiver(user_logged_in)
def log_user_logged_in_success(sender, request, user, **kwargs):
    LoginHistory.objects.create(
        ip=RequestInfoHelper.get_client_ip(request),
        email=user.email,
        agent=RequestInfoHelper.get_user_agent_info(request),
        logged=True)


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, request, credentials, **kwargs):
    email = credentials.get('email', credentials.get('username'))

    LoginHistory.objects.create(
        ip=RequestInfoHelper.get_client_ip(request),
        email=email,
        agent=RequestInfoHelper.get_user_agent_info(request),
        logged=False)
