from django.db import models
from django.utils.text import slugify

from utils.produtcts import primary_image_path, additional_image_path


# ---------------------------------------------------------------------
class ProductDetail(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductBrand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="brands/logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductionCountry(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3, blank=True)
    region = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductMaterial(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    primary_image = models.ImageField(
        upload_to=primary_image_path, blank=True, null=True
    )
    categories = models.ManyToManyField(Category, related_name="products")
    material = models.ForeignKey(
        ProductMaterial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    country = models.ForeignKey(
        ProductionCountry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    tags = models.ManyToManyField(
        Tags,
        blank=True,
        related_name="products",
    )
    slug = models.SlugField(unique=True)
    # SEO metadata
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="additional_images"
    )
    image = models.ImageField(upload_to=additional_image_path)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"


# ---------------------------------------------------------------------
class ProductDetailValue(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="details"
    )
    detail = models.ForeignKey(
        ProductDetail,
        on_delete=models.CASCADE,
        related_name="product_detail_values",
    )
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ("product", "detail")

    def __str__(self):
        return f"{self.product.name} - {self.detail.name}: {self.value}"


# ---------------------------------------------------------------------
class ProductCollection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    featured_image = models.ImageField(
        upload_to="collections/images/", blank=True, null=True
    )
    products = models.ManyToManyField(Product, related_name="collections")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
