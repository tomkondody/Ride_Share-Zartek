from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Ride


class RideTests(APITestCase):

    def setUp(self):
        self.rider = User.objects.create_user(username="rider", password="pass123")
        self.driver = User.objects.create_user(username="driver", password="pass123")

        # login rider
        response = self.client.post("/api/users/login/", {
            "username": "rider",
            "password": "pass123"
        })
        self.rider_token = response.data["access"]

    def authenticate_rider(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.rider_token)

    def authenticate_driver(self):
        response = self.client.post("/api/users/login/", {
            "username": "driver",
            "password": "pass123"
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_create_ride(self):
        self.authenticate_rider()

        data = {
            "pickup_location": "City",
            "dropoff_location": "Mall"
        }

        response = self.client.post("/api/rides/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "REQUESTED")

    def test_driver_accept_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="City",
            dropoff_location="Mall"
        )

        self.authenticate_driver()

        response = self.client.post(f"/api/rides/{ride.id}/accept/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["driver"])

    def test_start_ride(self):
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="City",
            dropoff_location="Mall"
        )

        self.authenticate_rider()

        response = self.client.post(f"/api/rides/{ride.id}/start/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "STARTED")
