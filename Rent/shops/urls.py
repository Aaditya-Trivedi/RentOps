from django.urls import path
from .views import create_shop

urlpatterns = [
    path('create/', create_shop, name='create_shop'),
]
