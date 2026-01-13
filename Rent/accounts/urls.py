from django.urls import path
from .views import shop_login, shop_logout

urlpatterns = [
    path('shop/login/', shop_login, name='shop_login'),
    path('shop/logout/', shop_logout, name='shop_logout'),
]
