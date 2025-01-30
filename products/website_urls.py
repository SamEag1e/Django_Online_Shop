from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list_user"),
    path("<str:slug>/", views.product_single, name="product_detail"),
]
