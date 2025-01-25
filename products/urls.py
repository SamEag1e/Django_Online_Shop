from django.urls import path
from .views import (
    product_brand,
    product_detail,
    product_country,
    product_material,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)


urlpatterns = []

urlpatterns = [
    path(
        "brand/",
        product_brand.list_view().as_view(),
        name="brand_list",
    ),
    path(
        "brand/create/",
        product_brand.create_view().as_view(),
        name="brand_create",
    ),
    path(
        "brand/<int:pk>/update/",
        product_brand.update_view().as_view(),
        name="brand_update",
    ),
    path(
        "brand/<int:pk>/delete/",
        product_brand.delete_view().as_view(),
        name="brand_delete",
    ),
    path("detail/", product_detail.list_view().as_view(), name="detail_list"),
    path(
        "detail/create/",
        product_detail.create_view().as_view(),
        name="detail_create",
    ),
    path(
        "detail/<int:pk>/update/",
        product_detail.update_view().as_view(),
        name="detail_update",
    ),
    path(
        "detail/<int:pk>/delete/",
        product_detail.delete_view().as_view(),
        name="detail_delete",
    ),
    path(
        "country/",
        product_country.list_view().as_view(),
        name="country_list",
    ),
    path(
        "country/create/",
        product_country.create_view().as_view(),
        name="country_create",
    ),
    path(
        "country/<int:pk>/update/",
        product_country.update_view().as_view(),
        name="country_update",
    ),
    path(
        "country/<int:pk>/delete/",
        product_country.delete_view().as_view(),
        name="country_delete",
    ),
    path(
        "material/",
        product_material.list_view().as_view(),
        name="material_list",
    ),
    path(
        "material/create/",
        product_material.create_view().as_view(),
        name="material_create",
    ),
    path(
        "material/<int:pk>/update/",
        product_material.update_view().as_view(),
        name="material_update",
    ),
    path(
        "material/<int:pk>/delete/",
        product_material.delete_view().as_view(),
        name="material_delete",
    ),
    path("list/", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]
