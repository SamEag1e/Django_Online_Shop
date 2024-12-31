from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from utils.otp import (
    phone_number_validation,
    second_send_otp_validation,
    verify_otp,
)

from .models import CustomUser


# ---------------------------------------------------------------------
def customer_logout(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید.")
    return redirect("home")


# ---------------------------------------------------------------------
def customer_login(request):
    phone_number = request.POST.get("phone_number")

    if not request.method == "POST":
        return render(request, "login/login.html")

    is_valid, message = phone_number_validation(phone_number)
    if not is_valid:
        messages.error(request, message)
        return render(request, "login/login.html")

    success, message = second_send_otp_validation(
        phone_number, "customer_login"
    )
    if success:
        request.session["phone_number"] = phone_number
        messages.success(request, message)
        return redirect("customer_otp_check")

    messages.error(request, message)
    return render(request, "login/login.html")


# ---------------------------------------------------------------------
def customer_otp_check(request):
    phone_number = request.session.get("phone_number")
    otp_code = "".join(
        [request.POST.get(f"otp_digit_{i}", "") for i in range(1, 7)]
    )

    if not request.method == "POST":
        return render(request, "login/otp-sms.html")

    is_valid, message = verify_otp(phone_number, otp_code, "customer_login")
    if is_valid:
        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        login(request, user)
        messages.success(request, message)
        del request.session["phone_number"]
        return redirect("home")

    # not is_valid
    messages.error(request, message)
    if message in (
        "کد وارد شده اشتباه است.",
        "کد یکبار مصرف ارسال شده را وارد کنید.",
    ):
        return render(request, "login/otp-sms.html")

    return redirect("customer_login")


# ---------------------------------------------------------------------
def profile(request):
    return render(request, "website/panel/profile.html")


# ---------------------------------------------------------------------
def edit_profile(request):
    if not request.method == "POST":
        return render(request, "website/panel/profile-edit.html")
    return render(request, "website/panel/profile-edit.html")


# ---------------------------------------------------------------------
def alerts(request):
    if not request.method == "POST":
        return render(request, "website/panel/alerts.html")
    return render(request, "website/panel/alerts.html")


# ---------------------------------------------------------------------
def alert_detail(request):
    if not request.method == "POST":
        return render(request, "website/panel/alert-detail.html")
    return render(request, "website/panel/alert-detail.html")


# ---------------------------------------------------------------------
def orders(request):
    if not request.method == "POST":
        return render(request, "website/panel/orders.html")
    return render(request, "website/panel/orders.html")


# ---------------------------------------------------------------------
def order_detail(request):
    if not request.method == "POST":
        return render(request, "website/panel/order-detail.html")
    return render(request, "website/panel/order-detail.html")


# ---------------------------------------------------------------------
def addresses(request):
    if not request.method == "POST":
        return render(request, "website/panel/addresses.html")
    return render(request, "website/panel/addresses.html")


# ---------------------------------------------------------------------
def edit_address(request):
    if not request.method == "POST":
        return render(request, "website/panel/address-edit.html")
    return render(request, "website/panel/address-edit.html")


# ---------------------------------------------------------------------
def create_address(request):
    if not request.method == "POST":
        return render(request, "website/panel/address-create.html")
    return render(request, "website/panel/address-create.html")


# ---------------------------------------------------------------------
def favorites(request):
    if not request.method == "POST":
        return render(request, "website/panel/favorites.html")
    return render(request, "website/panel/favorites.html")


# ---------------------------------------------------------------------
def tickets(request):
    if not request.method == "POST":
        return render(request, "website/panel/tickets.html")
    return render(request, "website/panel/tickets.html")


# ---------------------------------------------------------------------
def ticket_detail(request):
    if not request.method == "POST":
        return render(request, "website/panel/ticket-detail.html")
    return render(request, "website/panel/ticket-detail.html")


# ---------------------------------------------------------------------
def create_ticket(request):
    if not request.method == "POST":
        return render(request, "website/panel/ticket-create.html")
    return render(request, "website/panel/ticket-create.html")
