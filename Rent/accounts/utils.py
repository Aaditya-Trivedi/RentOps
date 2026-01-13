from django.utils import timezone
from django.core.mail import send_mail
from .models import FailedLoginAttempt, LoginLog


def record_failed_attempt(email, user_type):
    record, created = FailedLoginAttempt.objects.get_or_create(
        user_email=email,
        user_type=user_type
    )

    record.attempt_count += 1
    record.last_attempt = timezone.now()

    if record.attempt_count >= 3:
        record.is_locked = True

    record.save()


def reset_failed_attempts(email, user_type):
    FailedLoginAttempt.objects.filter(
        user_email=email,
        user_type=user_type
    ).update(
        attempt_count=0,
        is_locked=False
    )


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
    ).update(
        logout_time=timezone.now()
    )


def send_login_alert(email):
    send_mail(
        subject="Login Alert",
        message="Your account was logged in successfully.",
        from_email="noreply@clothrental.com",
        recipient_list=[email],
        fail_silently=True
    )




