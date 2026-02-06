from rest_framework import serializers
from .models import Ride


class RideCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = ['id', 'pickup_location', 'dropoff_location']

class RideListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = '__all__'

class RideStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["id", "status"]

class RideDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"

class RideAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["id", "driver", "status"]
