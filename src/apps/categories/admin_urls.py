from django.urls import path
from .views import (
    ProductCategoryCreateView,
    ProductCategoryUpdateView,
    ProductCategoryDeleteView,
    ProductCategoryTreeView,
)

urlpatterns = [
    path("tree/", ProductCategoryTreeView.as_view(), name="category_tree"),
    path(
        "create/", ProductCategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "update/<int:pk>/",
        ProductCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "delete/<int:pk>/",
        ProductCategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
