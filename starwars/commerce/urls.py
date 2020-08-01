from django.urls import path

from . import views

urlpatterns = [
    path("order/", views.OrderApi.as_view(), name="tool"),
    path("tools/", views.ToolApi.as_view(), name="tool"),
]
