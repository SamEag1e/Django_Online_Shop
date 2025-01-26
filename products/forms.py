from django import forms
from .models import Product, ProductAdditionalImage, ProductDetailValue


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("rates", "sales", "slug")


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
