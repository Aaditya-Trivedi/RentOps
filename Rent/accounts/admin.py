from django.contrib import admin
from .models import (
    PlatformAdmin,
    SubscriptionPlan,
    Shop,
    ShopSubscription,
    LoginLog,
    FailedLoginAttempt,
    NotificationLog
)

@admin.register(PlatformAdmin)
class PlatformAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('email',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'price', 'duration_days', 'max_items')
    search_fields = ('plan_name',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'owner_name', 'email', 'database_name', 'is_active')
    search_fields = ('shop_name', 'email')
    list_filter = ('is_active',)


@admin.register(ShopSubscription)
class ShopSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('shop', 'subscription', 'start_date', 'end_date', 'status')
    list_filter = ('status',)


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_type', 'login_time', 'logout_time', 'ip_address')
    search_fields = ('user_email',)


@admin.register(FailedLoginAttempt)
class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_type', 'attempt_count', 'is_locked')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'type', 'status', 'sent_at')
