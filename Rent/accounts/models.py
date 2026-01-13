from django.db import models
from datetime import timedelta
from django.utils.timezone import now


class PlatformAdmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SubscriptionPlan(models.Model):
    plan_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_items = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_name


class Shop(models.Model):
    shop_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    database_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

class ShopSubscription(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(default=now)
    end_date = models.DateField(blank=True)
    status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.subscription.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.shop.shop_name} - {self.subscription.plan_name}"


class LoginLog(models.Model):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SHOP', 'Shop'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    user_email = models.EmailField()
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user_email} ({self.user_type})"


class FailedLoginAttempt(models.Model):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SHOP', 'Shop'),
    )

    user_email = models.EmailField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    attempt_count = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_email} - {self.attempt_count}"


class NotificationLog(models.Model):
    NOTIFICATION_TYPE = (
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
    )

    recipient = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE)
    message = models.TextField()
    status = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.type}"

from django.db import models

# Create your models here.
