from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import LoginLog, FailedLoginAttempt, Shop


MAX_ATTEMPTS = 3


def log_login(email, user_type, ip):
    LoginLog.objects.create(
        user_email=email,
        user_type=user_type,
        login_time=timezone.now(),
        ip_address=ip
    )


def log_logout(email, user_type):
    LoginLog.objects.filter(
        user_email=email,
        user_type=user_type,
        logout_time__isnull=True
    ).update(logout_time=timezone.now())


def handle_failed_attempt(email, user_type):
    obj, _ = FailedLoginAttempt.objects.get_or_create(
        user_email=email,
        user_type=user_type
    )
    obj.attempt_count += 1
    obj.last_attempt = timezone.now()

    if obj.attempt_count >= MAX_ATTEMPTS:
        obj.is_locked = True
        if user_type == 'SHOP':
            Shop.objects.filter(email=email).update(is_active=False)

    obj.save()
    return obj.is_locked


def reset_failed_attempt(email, user_type):
    FailedLoginAttempt.objects.filter(
        user_email=email,
        user_type=user_type
    ).delete()


def send_login_email(email):
    send_mail(
        subject="Login Alert",
        message="You have successfully logged in.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True
    )
