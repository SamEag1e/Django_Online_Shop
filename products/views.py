from utils.view_helper import DynamicCRUDViewGenerator
from .models import (
    ProductBrand,
    ProductDetail,
    ProductCountry,
    ProductMaterial,
)


product_brand = DynamicCRUDViewGenerator(
    model=ProductBrand,
    success_url_name="brand_list",
    templates={
        "list": "brands/productbrand_list.html",
        "create": "brands/productbrand_form.html",
        "update": "brands/productbrand_form.html",
        "delete": "brands/productbrand_confirm_delete.html",
    },
    context_object_name="brands",
    fields=["name", "slug", "logo", "description"],
)


product_detail = DynamicCRUDViewGenerator(
    model=ProductDetail,
    success_url_name="detail_list",
    templates={
        "list": "product_details/productdetail_list.html",
        "create": "product_details/productdetail_form.html",
        "update": "product_details/productdetail_form.html",
        "delete": "product_details/productdetail_confirm_delete.html",
    },
    context_object_name="details",
    fields=["name"],
)

product_country = DynamicCRUDViewGenerator(
    model=ProductCountry,
    success_url_name="country_list",
    templates={
        "list": "product_country/productcountry_list.html",
        "create": "product_country/productcountry_form.html",
        "update": "product_country/productcountry_form.html",
        "delete": "product_country/productcountry_confirm_delete.html",
    },
    context_object_name="countries",
    fields=["name"],
)
product_material = DynamicCRUDViewGenerator(
    model=ProductMaterial,
    success_url_name="material_list",
    templates={
        "list": "product_material/productmaterial_list.html",
        "create": "product_material/productmaterial_form.html",
        "update": "product_material/productmaterial_form.html",
        "delete": "product_material/productmaterial_confirm_delete.html",
    },
    context_object_name="materials",
    fields=["name"],
)
