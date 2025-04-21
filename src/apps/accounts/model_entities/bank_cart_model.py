from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BankCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_number = models.CharField(max_length=16)
    shaba_number = models.CharField(max_length=26)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bank cart for {self.user.username} - {self.cart_number}"
