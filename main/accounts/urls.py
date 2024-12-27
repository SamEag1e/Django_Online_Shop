from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("otp/", views.customer_otp_check, name="customer_otp_check"),
    path("logout/", views.customer_logout, name="customer_logout"),
]
