from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from utils.view_helper import DynamicCRUDViewGenerator
from .models import (
    ProductBrand,
    ProductDetail,
    ProductCountry,
    ProductMaterial,
    Product,
)
from .forms import (
    ProductForm,
    ProductAdditionalImageFormset,
    ProductDetailValueFormset,
)

product_brand = DynamicCRUDViewGenerator(
    model=ProductBrand,
    success_url_name="brand_list",
    templates={
        "list": "admin/product_brand/productbrand_list.html",
        "create": "admin/product_brand/productbrand_form.html",
        "update": "admin/product_brand/productbrand_form.html",
        "delete": "admin/product_brand/productbrand_confirm_delete.html",
    },
    context_object_name="brands",
    fields=["name", "slug", "logo", "description"],
)


product_detail = DynamicCRUDViewGenerator(
    model=ProductDetail,
    success_url_name="detail_list",
    templates={
        "list": "admin/product_detail/productdetail_list.html",
        "create": "admin/product_detail/productdetail_form.html",
        "update": "admin/product_detail/productdetail_form.html",
        "delete": "admin/product_detail/productdetail_confirm_delete.html",
    },
    context_object_name="details",
    fields=["name"],
)

product_country = DynamicCRUDViewGenerator(
    model=ProductCountry,
    success_url_name="country_list",
    templates={
        "list": "admin/product_country/productcountry_list.html",
        "create": "admin/product_country/productcountry_form.html",
        "update": "admin/product_country/productcountry_form.html",
        "delete": "admin/product_country/productcountry_confirm_delete.html",
    },
    context_object_name="countries",
    fields=["name"],
)
product_material = DynamicCRUDViewGenerator(
    model=ProductMaterial,
    success_url_name="material_list",
    templates={
        "list": "admin/product_material/productmaterial_list.html",
        "create": "admin/product_material/productmaterial_form.html",
        "update": "admin/product_material/productmaterial_form.html",
        "delete": "admin/product_material/productmaterial_confirm_delete.html",
    },
    context_object_name="materials",
    fields=["name"],
)


class ProductListView(ListView):
    model = Product
    template_name = "admin/product/product_list.html"
    context_object_name = "products"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "admin/product/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ProductAdditionalImageFormset(
                self.request.POST, self.request.FILES, instance=self.object
            )
            context["detail_formset"] = ProductDetailValueFormset(
                self.request.POST, instance=self.object
            )
            return context
        context["image_formset"] = ProductAdditionalImageFormset(
            instance=Product()
        )
        context["detail_formset"] = ProductDetailValueFormset(
            instance=Product()
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        detail_formset = context["detail_formset"]
        if (
            form.is_valid()
            and image_formset.is_valid()
            and detail_formset.is_valid()
        ):
            self.object = form.save()
            image_formset.instance = self.object
            detail_formset.instance = self.object
            image_formset.save()
            detail_formset.save()
            return redirect("product_list")
        return self.form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "admin/product/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ProductAdditionalImageFormset(
                self.request.POST, self.request.FILES, instance=self.object
            )
            context["detail_formset"] = ProductDetailValueFormset(
                self.request.POST, instance=self.object
            )
            return context
        context["image_formset"] = ProductAdditionalImageFormset(
            instance=self.object
        )
        context["detail_formset"] = ProductDetailValueFormset(
            instance=self.object
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        detail_formset = context["detail_formset"]
        if (
            form.is_valid()
            and image_formset.is_valid()
            and detail_formset.is_valid()
        ):
            self.object = form.save()
            image_formset.save()
            detail_formset.save()
            return redirect("product_list")
        return self.form_invalid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "admin/product/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
