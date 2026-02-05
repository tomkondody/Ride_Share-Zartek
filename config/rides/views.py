from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Ride
from .serializers import RideCreateSerializer


class RideViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = RideCreateSerializer(data=request.data)

        if serializer.is_valid():
            ride = serializer.save(rider=request.user)
            return Response(
                {"message": "Ride created", "ride_id": ride.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
