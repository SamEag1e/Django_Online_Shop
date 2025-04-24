from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("otp/", views.user_otp_check, name="user_otp_check"),
    path("logout/", views.user_logout, name="user_logout"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    # path("alerts/", include("alerts.urls")),
    # path("tickets/", include("tickets.urls")),
    # path("orders/", include("orders.urls")),
    # path("favorites/", include("wishlists.urls")),
    path("", views.user_dashboard, name="home"),
]
