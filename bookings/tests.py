from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from vehicles.models import Vehicle

from .models import Booking


class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="123_pass")

        self.vehicle_data = {
            "owner": self.user,
            "make": "Test Vehicle",
            "model": "test-model",
            "year": 2024,
            "plate": "test-plate",
        }

        self.vehicle = Vehicle.objects.create(**self.vehicle_data)

        self.bookings = []

        self.bookings_data = [
            {
                "vehicle": self.vehicle,
                "start_date": date(2024, 10, 1),
                "end_date": date(2024, 10, 2),
                "booking_user": self.user,
            },
            {
                "vehicle": self.vehicle,
                "start_date": date(2024, 10, 5),
                "end_date": date(2024, 10, 7),
                "booking_user": self.user,
            }
        ]

        for data in self.bookings_data:
            self.bookings.append(Booking.objects.create(**data))

        self.bookings_url = reverse("bookings")

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)

    def test_list_bookings_unauthenticated(self):
        response = self.client.get(self.bookings_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_bookings(self):
        self.authenticate_user()
        response = self.client.get(self.bookings_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_booking_unauthenticated(self):
        response = self.create_booking()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking(self):
        self.authenticate_user()
        response = self.create_booking()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.count() == 3)

    def test_create_overlapping_booking(self):
        self.authenticate_user()
        response = self.create_overlapped_booking()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_booking(self):
        data = {
            "vehicle": self.vehicle.pk,
            "start_date": date(2024, 12, 10),
            "end_date": date(2024, 12, 11),
            "booking_user": self.user.pk,
        }

        return self.client.post(self.bookings_url, data)

    def create_overlapped_booking(self):
        data = {
            "vehicle": self.vehicle.pk,
            "start_date": date(2024, 10, 6),
            "end_date": date(2024, 10, 8),
            "booking_user": self.user.pk,
        }

        return self.client.post(self.bookings_url, data)
