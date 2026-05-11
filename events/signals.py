from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import AuditLog, Profile

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="Login Successful",
        ip_address=get_client_ip(request)
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    AuditLog.objects.create(
        user=None,
        action=f"Login Failed for username: {credentials.get('username')}",
        ip_address=get_client_ip(request)
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)