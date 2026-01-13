from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_cloth, name='add_cloth'),
    path('barcode/download/<str:code>/', views.download_barcode, name='download_barcode'),
]
