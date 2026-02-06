from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class UserAuthTests(APITestCase):

    def test_user_registration(self):
        data = {
            "username": "testuser1",
            "password": "testpass123",
            "email": "testuser1@example.com",
        }

        response = self.client.post("/api/users/register/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser1").exists())

    def test_user_login(self):
        User.objects.create_user(username="testuser2", password="testpass123")

        data = {
            "username": "testuser2",
            "password": "testpass123"
        }

        response = self.client.post("/api/users/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
