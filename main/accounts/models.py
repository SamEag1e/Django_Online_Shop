from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# ---------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    # -----------------------------------------------------------------
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    # -----------------------------------------------------------------
    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self.create_user(
            phone_number=phone_number, password=password, **extra_fields
        )


# ---------------------------------------------------------------------
class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = "phone_number"

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
