from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("otp/", views.admin_otp_check, name="admin_otp_check"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("test/", views.test, name="hello"),
]
