from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("otp/", views.customer_otp_check, name="customer_otp_check"),
    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/otp/", views.admin_otp_check, name="admin_otp_check"),
]
