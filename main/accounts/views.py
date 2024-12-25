from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import CustomUser
from .utils import send_otp, verify_otp, base_send_otp_validation


# ---------------------------------------------------------------------
def customer_login(request):
    if not request.method == "POST":
        return render(request, "login/login.html")

    phone_number = request.POST.get("phone_number")

    success, message = send_otp(phone_number, "customer_login")
    if success:
        request.session["phone_number"] = phone_number
        messages.success(request, message)
        return redirect("customer_otp_check")
    messages.error(request, message)
    return render(request, "login/login.html")


# ---------------------------------------------------------------------
def customer_otp_check(request):
    if not request.method == "POST":
        return render(request, "login/otp-sms.html")

    phone_number = request.session.get("phone_number")
    otp_code = "".join(
        [request.POST.get(f"otp_digit_{i}", "") for i in range(1, 7)]
    )
    is_valid, message = verify_otp(phone_number, otp_code, "customer_login")

    if is_valid:
        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        login(request, user)
        messages.success(request, message)
        del request.session["phone_number"]
        return redirect("home")

    messages.error(request, message)
    if message in (
        "کد وارد شده اشتباه است.",
        "کد یکبار مصرف ارسال شده را وارد کنید.",
    ):
        return render(request, "login/otp-sms.html")
    return redirect("customer_login")


# ---------------------------------------------------------------------
def admin_login(request):
    if not request.method == "POST":
        return render(request, "login/login.html")

    phone_number = request.POST.get("phone_number")

    is_base_valid, message = base_send_otp_validation(phone_number)
    if not is_base_valid:
        messages.error(request, message)
        return render(request, "login/login.html")

    user = CustomUser.objects.filter(phone_number=phone_number).first()
    if user is None or not user.is_staff:
        messages.error(request, "شماره وارد شده به عنوان ادمین یافت نشد.")
        return render(request, "login/login.html")

    success, message = send_otp(phone_number, "admin_login")
    if success:
        request.session["phone_number"] = phone_number
        messages.success(request, message)
        return redirect("admin_otp_check")

    messages.error(request, message)
    return render(request, "login/login.html")


# ---------------------------------------------------------------------
def admin_otp_check(request):
    pass


# ---------------------------------------------------------------------
def add_admin(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.error(
            request, "You don't have permission to create admin accounts."
        )
        return redirect("home")

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        is_superuser = request.POST.get("is_superuser") == "on"

        if not password:
            messages.error(request, "Password is required.")
            return redirect("add_admin")

        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        user.is_staff = True
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()

        messages.success(
            request,
            f"{'Superuser' if is_superuser else 'Staff'} account created successfully.",
        )
        return redirect("admin_dashboard")

    return render(request, "accounts/add_admin.html")


# ---------------------------------------------------------------------
def user_logout(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید.")
    return redirect("home")
