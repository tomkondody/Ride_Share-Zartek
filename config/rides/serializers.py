from rest_framework import serializers
from .models import Ride


class RideCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = ['id', 'pickup_location', 'dropoff_location']
