from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Address(models.Model):
    label = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.province}"
