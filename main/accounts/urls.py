from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("login-otp/", views.login_otp, name="login_otp"),
]
