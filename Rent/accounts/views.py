from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from .services import (
    log_login, handle_failed_attempt,
    reset_failed_attempt, send_login_email,
    log_logout
)

from .models import PlatformAdmin, Shop, FailedLoginAttempt
from .utils import (
    record_failed_attempt,
    reset_failed_attempts,
    log_login,
    send_login_alert,
    log_logout
)

def login_view(request, user_type):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        ip = request.META.get('REMOTE_ADDR')

        # check lock status
        lock = FailedLoginAttempt.objects.filter(
            user_email=email,
            user_type=user_type,
            is_locked=True
        ).first()

        if lock:
            messages.error(request, "Account locked due to multiple failed attempts.")
            return redirect('login')

        if user_type == 'ADMIN':
            user = PlatformAdmin.objects.filter(email=email, password=password).first()
        else:
            user = Shop.objects.filter(email=email, is_active=True).first()

        if user:
            reset_failed_attempts(email, user_type)
            log_login(email, user_type, ip)
            send_login_alert(email)

            request.session['user_email'] = email
            request.session['user_type'] = user_type

            return redirect('dashboard')

        else:
            record_failed_attempt(email, user_type)
            messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html')

def logout_view(request):
    email = request.session.get('user_email')
    user_type = request.session.get('user_type')

    if email and user_type:
        log_logout(email, user_type)

    request.session.flush()
    return redirect('login')

def shop_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        ip = request.META.get('REMOTE_ADDR')

        try:
            shop = Shop.objects.get(email=email)

            if not shop.is_active:
                return HttpResponseForbidden("Account is locked")

            if check_password(password, shop.password):
                reset_failed_attempt(email, 'SHOP')
                log_login(email, 'SHOP', ip)
                send_login_email(email)
                request.session['shop_id'] = shop.id
                return redirect('shop_dashboard')
            else:
                locked = handle_failed_attempt(email, 'SHOP')
                if locked:
                    messages.error(request, "Account locked after 3 attempts")
                else:
                    messages.error(request, "Invalid credentials")

        except Shop.DoesNotExist:
            messages.error(request, "Invalid credentials")

    return render(request, 'accounts/shop_login.html')

def shop_logout(request):
    email = request.session.get('shop_email')
    log_logout(email, 'SHOP')
    request.session.flush()
    return redirect('shop_login')