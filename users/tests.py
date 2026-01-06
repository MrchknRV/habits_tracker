from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationTest(APITestCase):
    def test_register_user_success(self):
        url = reverse("users:register")
        data = {"email": "test@example.com", "password": "testpass123456", "password2": "testpass123456"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"], "test@example.com")

    def test_register_password_mismatch(self):
        url = reverse("users:register")
        data = {"email": "test2@example.com", "password": "pass1", "password2": "pass2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
