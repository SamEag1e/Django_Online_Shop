from django.utils.timezone import now, timedelta


# ---------------------------------------------------------------------
def default_otp_expiry():
    return now() + timedelta(minutes=5)


# ---------------------------------------------------------------------
def default_otp_attemps_expiry():
    return now() + timedelta(minutes=30)
