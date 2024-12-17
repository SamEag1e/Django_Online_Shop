from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.utils.timezone import now, timedelta
from .models import OTPRequest, CustomUser
from .utils import generate_otp, send_sms


# ---------------------------------------------------------------------
def send_otp(phone_number, otp_type):
    if not phone_number:
        return False, "Phone number is required."

    if not (
        phone_number.startswith("+")
        and phone_number[1:].isdigit()
        and 10 <= len(phone_number) <= 15
    ):

        return (
            False,
            "شماره وارد شده اشتباه است. با فرمت +999999999 شماره را وارد کنید.",
        )

    otp_request, _ = OTPRequest.objects.get_or_create(
        phone_number=phone_number
    )
    if otp_request.otp_attemps >= 3 and now() < otp_request.otp_attemps_expiry:
        time_difference = otp_request.otp_attemps_expiry - now()
        minutes_left = time_difference.total_seconds() / 60
        minutes_left = round(minutes_left)
        return (
            False,
            "تعداد دفعات ارسال رمز یکبار مصرف به پایان رسیده است. "
            f"بعد از {minutes_left} دقیقه امتحان کنید.",
        )

    if now() >= otp_request.otp_attemps_expiry:
        otp_request.otp_attemps = 0

    otp_request.otp_type = otp_type
    otp_request.otp_attemps += 1
    otp_request.otp_attemps_expiry = now() + timedelta(minutes=30)
    otp_request.otp_code = generate_otp()
    otp_request.otp_expiry = now() + timedelta(minutes=5)
    otp_request.save()

    send_sms(otp_request.phone_number, otp_request.otp_code)
    return True, "رمز یکبار مصرف به شماره شما ارسال شد."


# ---------------------------------------------------------------------
def verify_otp(phone_number, otp_code, otp_type):
    if not phone_number or not otp_code:
        return False, "Phone number and OTP code are required."

    otp_request = OTPRequest.objects.filter(phone_number=phone_number).first()
    if not otp_request:
        return False, "OTP request not found for this phone number."

    if now() > otp_request.otp_expiry:
        return False, "OTP has expired."

    if otp_request.otp_type != otp_type:
        return False, "Invalid OTP type."

    if otp_request.otp_code != otp_code:
        return False, "Invalid OTP."

    otp_request.delete()
    return True, "OTP is valid."


# ---------------------------------------------------------------------
def customer_login(request):
    if not request.method == "POST":
        return render(request, "website/login.html")

    phone_number = request.POST.get("phone_number")
    if not phone_number:
        messages.error(request, "شماره تلفن خود را وارد کنید.")
        return redirect("customer_login")
    success, message = send_otp(phone_number, "customer_login")
    if success:
        messages.success(request, message)
        return redirect("customer_otp")
    messages.error(request, message)
    return redirect("customer_login")


# ---------------------------------------------------------------------
def customer_otp(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        otp_code = request.POST.get("otp_code")
        is_valid, message = verify_otp(
            phone_number, otp_code, "customer_login"
        )

        if not is_valid:
            messages.error(request, message)
            return redirect("customer_login")

        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        login(request, user)
        messages.success(request, "Logged in successfully.")
        return redirect("home")

    return render(request, "website/otp-sms.html")


# ---------------------------------------------------------------------
def admin_login(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        user = authenticate(
            request, phone_number=phone_number, password=password
        )
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Admin logged in successfully.")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials or not an admin.")

    return render(request, "accounts/admin_login.html")


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

        user, created = CustomUser.objects.get_or_create(
            phone_number=phone_number
        )
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
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")
