from django.urls import path

from .views import VehiclesView, SingleVehicleView

urlpatterns = [
    path("vehicles/", VehiclesView.as_view(), name="vehicles"),
    path("vehicles/<int:pk>", SingleVehicleView.as_view(), name="single_vehicle"),
]
