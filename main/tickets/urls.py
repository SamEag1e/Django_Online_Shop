from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_ticket, name="create_ticket"),
    path("list/", views.tickets, name="tickets"),
    path("detail/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("deactive/<int:pk>/", views.ticket_detail, name="ticket_detail"),
]
