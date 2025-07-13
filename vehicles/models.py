from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    plate = models.CharField(max_length=255)
    year = models.IntegerField()
    owner = models.ForeignKey(User, related_name="vehicle", on_delete=models.CASCADE)
