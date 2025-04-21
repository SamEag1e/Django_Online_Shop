from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.customer_login, name="customer_login"),
    path("otp/", views.customer_otp_check, name="customer_otp_check"),
    path("logout/", views.customer_logout, name="customer_logout"),
    path("profile/", views.profile, name="customer_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("alerts/", include("alerts.urls")),
    path("tickets/", include("tickets.urls")),
    path("addresses/", include("addresses.urls")),
    path("bank-carts/", include("bank_carts.urls")),
    path("orders/", include("orders.urls")),
    path("favorites/", include("wishlists.urls")),
    path("", views.profile, name="home"),
]
