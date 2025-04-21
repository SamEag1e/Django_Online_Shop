from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.orders, name="orders"),
    path("detail/<int:pk>/", views.order_detail, name="order_detail"),
]
