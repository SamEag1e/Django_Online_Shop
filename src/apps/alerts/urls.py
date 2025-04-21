from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.alerts, name="alerts"),
    path("detail/<int:pk>/", views.alert_detail, name="alert_detail"),
]
