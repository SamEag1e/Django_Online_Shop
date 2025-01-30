from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

from categories.models import Category
from rates.models import Rate
from .utils import primary_image_path, additional_image_path


# ---------------------------------------------------------------------
class ProductMaterial(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1
        while (
            ProductMaterial.objects.filter(slug=self.slug)
            .exclude(id=self.id)
            .exists()
        ):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductBrand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="brands/logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1
        while (
            ProductBrand.objects.filter(slug=self.slug)
            .exclude(id=self.id)
            .exists()
        ):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductCountry(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3, blank=True)
    region = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1
        while (
            ProductCountry.objects.filter(slug=self.slug)
            .exclude(id=self.id)
            .exists()
        ):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class ProductDetail(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    price = models.BigIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    primary_image = models.ImageField(
        upload_to=primary_image_path, blank=True, null=True
    )
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
        ProductCountry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    categories = models.ManyToManyField(
        Category, related_name="products", blank=True
    )
    # SEO metadata
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    # Not in admin form fields
    discount = models.SmallIntegerField(blank=True, null=True)
    sales = models.IntegerField(default=0)
    rates = GenericRelation(Rate, related_query_name="rates", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1
        while (
            Product.objects.filter(slug=self.slug).exclude(id=self.id).exists()
        ):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def discounted_price(self):
        discounted = self.price * (self.discount / 100.0)
        return round(discounted / 1000) * 1000


# ---------------------------------------------------------------------
class ProductAdditionalImage(models.Model):
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
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1
        while (
            ProductCollection.objects.filter(slug=self.slug)
            .exclude(id=self.id)
            .exists()
        ):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
