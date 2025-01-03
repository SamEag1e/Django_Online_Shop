from django.urls import path
from . import views

auth_url = [
    path("login/", views.customer_login, name="customer_login"),
    path("otp/", views.customer_otp_check, name="customer_otp_check"),
]
user_url = [
    path("logout/", views.customer_logout, name="customer_logout"),
    path("profile/", views.profile, name="customer_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("alerts/", views.alerts, name="alerts"),
    path("alert-detail/<int:pk>/", views.alert_detail, name="alert_detail"),
    path("tickets/", views.tickets, name="tickets"),
    path("ticket-detail/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("create-ticket/", views.create_ticket, name="create_ticket"),
    path("addresses/", views.addresses, name="addresses"),
    path("edit-address/<int:pk>/", views.edit_address, name="edit_address"),
    path("create-address/", views.create_address, name="create_address"),
    path("bank-carts/", views.bank_carts, name="bank_carts"),
    path(
        "edit-bank-cart/<int:pk>/",
        views.edit_bank_cart,
        name="edit_bank_carts",
    ),
    path(
        "create-bank-cart/", views.create_bank_cart, name="create_bank_carts"
    ),
    path("orders/", views.orders, name="orders"),
    path("order-detail/<int:pk>/", views.order_detail, name="order_detail"),
    path("favorites/", views.favorites, name="favorites"),
    path("", views.profile, name="home"),
]

urlpatterns = auth_url + user_url
