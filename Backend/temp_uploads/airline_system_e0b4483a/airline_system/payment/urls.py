# payment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('payment_page/<str:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
]
