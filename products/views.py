from django.shortcuts import render
from django.db.models import Count, Q, ExpressionWrapper, F, IntegerField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from utils.view_helper import DynamicCRUDViewGenerator
from categories.trees import get_category_and_descendants

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
from .utils import get_sorting_field

# ---------------------------------------------------------------------
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
    fields=["name", "logo", "description"],
)

# ---------------------------------------------------------------------
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
# ---------------------------------------------------------------------
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
    fields=["name", "country_code", "region"],
)
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
class ProductListView(ListView):
    model = Product
    template_name = "admin/product/product_list.html"
    context_object_name = "products"


# ---------------------------------------------------------------------
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "admin/product/product_confirm_delete.html"
    success_url = reverse_lazy("product_list_admin")


# ---------------------------------------------------------------------
class ProductFormView:
    model = Product
    form_class = ProductForm
    template_name = "admin/product/product_form.html"
    success_url = reverse_lazy("product_list_admin")

    def get_formsets(self):
        """Helper function to get the formsets."""
        return {
            "additional_image_formset": ProductAdditionalImageFormset(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
            ),
            "detail_value_formset": ProductDetailValueFormset(
                self.request.POST or None, instance=self.object
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = self.get_formsets()  # Get formsets
        context.update(formsets)  # Add formsets to context
        return context

    def form_valid(self, form):
        """Handles saving both the Product and the formsets."""
        context = self.get_context_data(form=form)
        additional_image_formset = context["additional_image_formset"]
        detail_value_formset = context["detail_value_formset"]

        if not (
            additional_image_formset.is_valid()
            and detail_value_formset.is_valid()
        ):
            return self.form_invalid(form)

        # Save Product instance (either create or update)
        self.object = form.save()

        # Save formsets associated with the Product instance
        additional_image_formset.instance = self.object
        detail_value_formset.instance = self.object
        additional_image_formset.save()
        detail_value_formset.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


# ---------------------------------------------------------------------
class ProductUpdateView(ProductFormView, UpdateView):
    pass


# ---------------------------------------------------------------------
class ProductCreateView(ProductFormView, CreateView):
    pass


# ########################### Website_views ###########################
# ---------------------------------------------------------------------
def filter_products(request):
    products = Product.objects.all()

    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    brand = request.GET.getlist("brand")
    material = request.GET.getlist("material")
    category = request.GET.getlist("category")
    search = request.GET.get("search", "")

    if search:
        products = products.filter(
            Q(name__icontains=search)
            | Q(sku__icontains=search)
            | Q(description__icontains=search)
        )
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand:
        products = products.filter(brand__slug__in=brand)
    if material:
        products = products.filter(material__slug__in=material)
    # Filter by category (using slugs) and include children's products
    if category:
        all_categories = get_category_and_descendants(category)
        products = products.filter(
            categories__slug__in=all_categories.values_list("slug", flat=True)
        )

    products = products.distinct().annotate(
        discounted_price=ExpressionWrapper(
            (F("price") * (1 - Coalesce(F("discount"), 0) / 100) / 1000)
            * 1000,
            output_field=IntegerField(),
        )
    )

    # Return both the filtered products and the selected filters
    return products, {
        "min_price": min_price,
        "max_price": max_price,
        "brand": brand,
        "material": material,
        "category": category,
    }


# ---------------------------------------------------------------------
def product_list(request):
    products, selected_filters = filter_products(request)

    order = get_sorting_field(request.GET.get("order", "most_recent"))

    # Pagination
    paginator = Paginator(products.order_by(order), 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    context = {
        "products": page_obj,
        "brands": ProductBrand.objects.annotate(
            product_count=Count("products")
        ),
        "materials": ProductMaterial.objects.annotate(
            product_count=Count("products")
        ),
        "selected_filters": selected_filters,
        "total_products": paginator.count,
        "start_index": page_obj.start_index(),
        "end_index": page_obj.end_index(),
    }
    return render(request, "website/product/product-list-user.html", context)


# ---------------------------------------------------------------------
def product_single(request, slug):
    return render(request, "website/product/product-list-user.html")
