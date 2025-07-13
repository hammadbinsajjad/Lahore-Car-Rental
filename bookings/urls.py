from django.urls import path

from .views import BookingsView

urlpatterns = [
    path("bookings/", BookingsView.as_view(), name="bookings")
]
