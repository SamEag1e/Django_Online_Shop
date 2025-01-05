from django.db import models
from .defaults import default_otp_attemps_expiry, default_otp_expiry


# ---------------------------------------------------------------------
class OTPRequest(models.Model):

    OTP_TYPE_CHOICES = [
        ("customer_login", "Customer Login"),
        ("admin_login", "Admin Login"),
        ("admin_register", "Admin Register"),
        ("password_change", "Password change"),
    ]
    phone_number = models.CharField(max_length=15, unique=True)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_attemps = models.PositiveIntegerField(default=0)
    otp_checks = models.PositiveIntegerField(default=0)
    otp_expiry = models.DateTimeField(default=default_otp_expiry)
    otp_attemps_expiry = models.DateTimeField(
        default=default_otp_attemps_expiry
    )

    # -----------------------------------------------------------------
    def __str__(self):
        return f"OTP for {self.phone_number}"
