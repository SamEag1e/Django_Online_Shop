from django.utils.timezone import now, timedelta

from shared.messages import get_res_obj
from .models import OTPRequest
from .utils import generate_otp


def send_otp_validate(phone_number, otp_type):
    otp_request, _ = OTPRequest.objects.get_or_create(
        phone_number=phone_number
    )

    if otp_request.attemps >= 3 and otp_request.attemps_expiry > now():
        return get_res_obj(False, "otp_send_attemps_expired")

    if now() >= otp_request.attemps_expiry:
        otp_request.attemps = 0

    otp_request.type = otp_type
    otp_request.checks = 0
    otp_request.attemps += 1
    otp_request.attemps_expiry = now() + timedelta(minutes=5)
    otp_request.code = generate_otp()
    otp_request.expiry = now() + timedelta(minutes=5)
    otp_request.save()

    return get_res_obj(True, "otp_send_success")


def verify_otp(phone_number, otp_code, otp_type):
    otp_request = OTPRequest.objects.filter(phone_number=phone_number).first()

    if not otp_request:
        return get_res_obj(False, "otp_not_found")

    if now() > otp_request.expiry:
        otp_request.code = None
        otp_request.save()
        return get_res_obj(False, "otp_expired")

    if otp_request.type != otp_type:
        return get_res_obj(False, "otp_diff_type")

    otp_request.checks += 1
    otp_request.save()

    if otp_request.checks > 5:
        otp_request.code = None
        otp_request.save()
        return get_res_obj(False, "otp_attemps_expired")

    if otp_request.code != otp_code:
        return get_res_obj(False, "otp_invalid")

    otp_request.delete()
    return get_res_obj(True, "otp_verify_success")
