from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("login-otp/", views.customer_otp, name="customer_otp"),
]
