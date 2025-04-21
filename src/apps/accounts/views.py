from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from shared.messages import get_res_obj
from apps.otps.services import send_otp_validate, verify_otp
from .models import CustomUser
from .utils import phone_number_validate


# ---------------------------------------------------------------------
def customer_logout(request):
    logout(request)
    messages.success(request, get_res_obj(True, "user_logout").get("msg"))
    return redirect("home")


# ---------------------------------------------------------------------
def customer_login(request):
    # TODO: If user is authenticated => profile or home
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
    # TODO: If user is authenticated => profile or home
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
