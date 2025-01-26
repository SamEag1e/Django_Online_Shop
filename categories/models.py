from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from .utils import get_slug


# ---------------------------------------------------------------------
class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    description = models.TextField(blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, allow_unicode=True
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def save(self, *args, **kwargs):
        slug = get_slug(self)
        if Category.objects.filter(slug=slug).exists():
            raise ValidationError(f"The slug '{slug}' already exists.")
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return " -> ".join(
            [
                ancestor.name
                for ancestor in self.get_ancestors(include_self=True)
            ]
        )
