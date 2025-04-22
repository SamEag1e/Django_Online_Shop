from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from otps.services import send_otp_validate, verify_otp
from shared.messages import get_res_obj
from .models import CustomUser
from .utils import phone_number_validate


def profile(request):
    return render(request, "user_panel/profile/profile.html")


def edit_profile(request):
    if not request.method == "POST":
        return render(request, "user_panel/profile/profile-edit.html")

    return render(request, "user_panel/profile/profile-edit.html")


def customer_logout(request):
    logout(request)
    messages.success(request, get_res_obj(True, "user_logout").get("msg"))

    return redirect("home")


def customer_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if not request.method == "POST":
        return render(request, "accounts/login.html")

    phone_number = request.POST.get("phone_number")
    validation = phone_number_validate(phone_number)

    if not validation.get("is_success"):
        messages.error(request, validation.get("msg"))

        return render(request, "accounts/login.html")

    validation = send_otp_validate(phone_number, "customer_login")

    if not validation.get("is_success"):
        messages.error(request, validation.get("msg"))

        return render(request, "accounts/login.html")

    request.session["phone_number"] = phone_number
    messages.success(request, validation.get("msg"))

    return redirect("customer_otp_check")


def customer_otp_check(request):
    if request.user.is_authenticated:
        return redirect("home")

    if not request.method == "POST":
        return render(request, "accounts/otp-sms.html")

    phone_number = request.session.get("phone_number")
    otp_code = "".join(
        [request.POST.get(f"otp_digit_{i}", "") for i in range(1, 7)]
    )

    validation = verify_otp(phone_number, otp_code, "customer_login")

    if validation.get("is_success"):
        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        login(request, user)
        messages.success(request, validation.get("msg"))
        del request.session["phone_number"]

        return redirect("home")

    messages.error(request, validation.get("msg"))
    if validation.get("msg_key") == "otp_invalid":
        return render(request, "accounts/otp-sms.html")

    return redirect("customer_login")
