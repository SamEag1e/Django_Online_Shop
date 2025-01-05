from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_address, name="create_address"),
    path("list/", views.addresses, name="addresses"),
    path("update/<int:pk>/", views.edit_address, name="edit_address"),
    path("delete/<int:pk>/", views.edit_address, name="edit_address"),
]
