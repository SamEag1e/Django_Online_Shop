from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_bank_cart, name="create_bank_carts"),
    path("list/", views.bank_carts, name="bank_carts"),
    path("update/<int:pk>/", views.edit_bank_cart, name="edit_bank_carts"),
    path("delete/<int:pk>/", views.edit_bank_cart, name="edit_bank_carts"),
]
