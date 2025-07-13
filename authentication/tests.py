from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_api = reverse("register")
        self.login_api = reverse("login")
        self.refresh_api = reverse("auth-refresh")
        self.user_data = {
            "username": "test_user",
            "password": "Pass@123",
        }

    def test_register(self):
        response = self.client.post(self.register_api, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.user_data["username"]).exists())

    def test_login(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.login_api, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]

    def test_auth_token_refresh(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.login_api, self.user_data)
        refresh_token = response.data["refresh"]
        response = self.client.post(self.refresh_api, {"refresh": refresh_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
