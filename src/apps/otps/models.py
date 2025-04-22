from django.db import models
from .utils import default_otp_attemps_expiry, default_otp_expiry


class OTPRequest(models.Model):
    OTP_TYPE_CHOICES = [
        ("customer_login", "Customer Login"),
        ("admin_login", "Admin Login"),
        ("admin_register", "Admin Register"),
        ("password_change", "Password change"),
    ]
    phone_number = models.CharField(max_length=15, unique=True)
    type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    code = models.CharField(max_length=6, blank=True, null=True)
    attemps = models.PositiveIntegerField(default=0)
    checks = models.PositiveIntegerField(default=0)
    expiry = models.DateTimeField(default=default_otp_expiry)
    attemps_expiry = models.DateTimeField(default=default_otp_attemps_expiry)

    def __str__(self):
        return f"OTP {self.type} for {self.phone_number}"
