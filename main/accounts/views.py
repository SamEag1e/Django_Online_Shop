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

    categories = [
        {"آشپزخانه": ["پارچ", "لیوان", "بشقاب"]},
        {"تزئینی": ["زیر دسته بندی", "زیر دسته بندی 2"]},
    ]
    menu_data = [
        {
            "title": "بر اساس دسته بندی",
            "sub_items": [
                "آشپزخانه",
                "تزئینی",
                "سکسی",
            ],
        },
        {
            "title": "بر اساس قیمت",
            "sub_items": [
                "گوشی تا 2 میلیون",
                "گوشی تا 5 میلیون",
                "گوشی تا 10 میلیون",
                "گوشی تا 12 میلیون",
                "گوشی تا 15 میلیون",
            ],
        },
        {
            "title": "بر اساس برند",
            "sub_items": ["پاشاباغچه", "اون یکی"],
        },
        {
            "title": "بر اساس کشور تولید کننده",
            "sub_items": ["ایران", "جین"],
        },
    ]

    return render(
        request,
        "website/website_base.html",
        context={"categories": categories, "menu_data": menu_data},
    )
    if not request.user_is_authenticated:
        return redirect("customer_login")
    if not request.method == "POST":
        return render(request, "html")
    f_name = request.get("frist_name", None)
    l_name = request.get("last_name", None)
    email = request.get("email", None)
