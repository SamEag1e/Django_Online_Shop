import random

from django.utils.timezone import now, timedelta

from accounts.models import OTPRequest


# ---------------------------------------------------------------------
def phone_number_validation(phone_number):
    if not phone_number:
        return False, "شماره موبایل خود را وارد کنید."

    if not (
        phone_number.startswith("0")
        and phone_number[1:].isdigit()
        and 10 <= len(phone_number) <= 15
    ):

        return (
            False,
            "شماره وارد شده اشتباه است. با فرمت 09123456789 شماره را وارد کنید.",
        )
    return True, "شماره وارد شده صحیح است."


# ---------------------------------------------------------------------
def second_send_otp_validation(phone_number, otp_type):
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
    otp_request.otp_checks = 0
    otp_request.otp_attemps += 1
    otp_request.otp_attemps_expiry = now() + timedelta(minutes=30)
    otp_request.otp_code = generate_otp()
    otp_request.otp_expiry = now() + timedelta(minutes=5)
    otp_request.save()

    send_sms(otp_request.phone_number, otp_request.otp_code)
    return True, "کد یکبار مصرف به شماره شما ارسال شد."


# ---------------------------------------------------------------------
def verify_otp(phone_number, otp_code, otp_type):
    if not phone_number:
        print("Verify", phone_number)
        return False, "شماره موبایل خود را وارد کنید."

    if not otp_code.isdigit():
        return False, "کد یکبار مصرف ارسال شده را وارد کنید."

    otp_request = OTPRequest.objects.filter(phone_number=phone_number).first()
    if not otp_request:
        return False, "برای شماره وارد شده کد یکبار مصرفی یافت نشد."

    if now() > otp_request.otp_expiry:
        otp_request.otp_code = None
        otp_request.save()
        return (
            False,
            "زمان استفاده از کد یکبار مصرف به پایان رسیده است. لطفاً دوباره درخواست کد کنید.",
        )

    if otp_request.otp_type != otp_type:
        return False, "نوع کد یکبار مصرف ارسال شده با درخواست شما متفاوت است."

    otp_request.otp_checks += 1
    otp_request.save()

    if otp_request.otp_checks > 5:
        otp_request.otp_code = None
        otp_request.save()
        return (
            False,
            "تعداد تلاش‌های شما به پایان رسیده است. لطفاً دوباره درخواست کنید.",
        )

    if otp_request.otp_code != otp_code:
        return False, "کد وارد شده اشتباه است."

    otp_request.delete()
    return True, "با موفقیت وارد شدید."


# ---------------------------------------------------------------------
def generate_otp():
    return str(random.randint(100000, 999999))


# ---------------------------------------------------------------------
def send_sms(phone_number, otp):
    # Send otp to the phone_number using
    # an external API.
    pass
