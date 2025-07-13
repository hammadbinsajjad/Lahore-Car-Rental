from django.contrib.auth.models import User
from django.db import models

from vehicles.models import Vehicle


class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    booking_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
