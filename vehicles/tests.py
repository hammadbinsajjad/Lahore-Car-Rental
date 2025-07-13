from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Vehicle


class BaseVehicleTests(APITestCase):
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

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)


class VehiclesTests(BaseVehicleTests):
    def setUp(self):
        super().setUp()
        self.vehicles_url = reverse("vehicles")

    def test_list_vehicles_unauthenticated(self):
        response = self.client.get(self.vehicles_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_vehicles(self):
        self.authenticate_user()
        response = self.client.get(self.vehicles_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_vehicle_unauthenticated(self):
        response = self.create_vehicle()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vehicle(self):
        self.authenticate_user()
        response = self.create_vehicle()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vehicle.objects.count() == 2)

    def create_vehicle(self):
        data = {
            "owner": self.user,
            "make": "Test Car 2",
            "model": "test-2-model",
            "year": 2023,
            "plate": "test-2-plate",
        }

        return self.client.post(self.vehicles_url, data)


class SingleVehicleTests(BaseVehicleTests):
    def setUp(self):
        super().setUp()
        self.single_vehicle_url = reverse("single_vehicle", args=[self.vehicle.pk])

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)

    def test_update_vehicle_unathenticated(self):
        response = self.update_vehicle({})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_vehicle(self):
        self.authenticate_user()

        updated_data = {"year": 2023}
        response = self.update_vehicle(updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for field, value in updated_data.items():
            self.assertEqual(response.data.get(field) or "Not Found", value)

    def update_vehicle(self, updated_data):
        data = {
            **self.vehicle_data,
            **updated_data
        }

        return self.client.put(self.single_vehicle_url, data)

    def test_delete_vehicle_unauthenticated(self):
        response = self.delete_vehicle()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_vehicle(self):
        self.authenticate_user()

        prev_vehicle_count = Vehicle.objects.count()

        response = self.delete_vehicle()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(Vehicle.objects.count(), prev_vehicle_count)

    def delete_vehicle(self):
        return self.client.delete(self.single_vehicle_url)
