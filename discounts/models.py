from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# ---------------------------------------------------------------------
class AbstractDiscount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    name = models.CharField(max_length=255)
    discount_type = models.CharField(
        max_length=20, choices=DISCOUNT_TYPE_CHOICES
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    max_usage_count = models.PositiveIntegerField(blank=True, null=True)
    current_usage_count = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductDiscount(AbstractDiscount):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


# ---------------------------------------------------------------------
class UserDiscount(AbstractDiscount):
    code = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(
        get_user_model(), related_name="discounts", blank=True
    )
    user_max_usage_count = models.PositiveIntegerField(blank=True, null=True)


# ---------------------------------------------------------------------
class UserDiscountUsage(models.Model):
    discount = models.ForeignKey(UserDiscount, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} used {self.discount}"
