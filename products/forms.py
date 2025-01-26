from django import forms
from django.contrib.contenttypes.models import ContentType

from categories.models import Category
from .models import Product, ProductAdditionalImage, ProductDetailValue


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "is_active",
            "name",
            "sku",
            "price",
            "quantity",
            "material",
            "brand",
            "country",
            "categories",
            "meta_title",
            "meta_description",
            "description",
            "primary_image",
        ]

    product_content_type = ContentType.objects.get_for_model(Product)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(
            content_type=ContentType.objects.get_for_model(Product)
        ),
        required=False,
    )


class ProductAdditionalImageForm(forms.ModelForm):
    class Meta:
        model = ProductAdditionalImage
        fields = ("image",)


class ProductDetailValueForm(forms.ModelForm):
    class Meta:
        model = ProductDetailValue
        fields = ("detail", "value")


ProductAdditionalImageFormset = forms.inlineformset_factory(
    Product,
    ProductAdditionalImage,
    form=ProductAdditionalImageForm,
    extra=1,
    can_delete=True,
)


ProductDetailValueFormset = forms.inlineformset_factory(
    Product,
    ProductDetailValue,
    form=ProductDetailValueForm,
    extra=1,
    can_delete=True,
)
