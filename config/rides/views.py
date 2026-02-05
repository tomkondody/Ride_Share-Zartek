from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Ride
from .serializers import RideCreateSerializer, RideListSerializer
from rest_framework.viewsets import ModelViewSet


class RideViewSet(ModelViewSet):

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

    def list(self, request):
        rides = Ride.objects.filter(rider=request.user)

        page = self.paginate_queryset(rides)
        if page is not None:
            serializer = RideListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RideListSerializer(rides, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            ride = Ride.objects.get(id=pk, rider=request.user)
        except Ride.DoesNotExist:
            return Response(
                {"error": "Ride not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RideListSerializer(ride)
        return Response(serializer.data)
