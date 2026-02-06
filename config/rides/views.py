from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Ride
from .serializers import RideCreateSerializer, RideListSerializer, RideDetailSerializer, RideLocationSerializer, RideStatusSerializer ,RideAcceptSerializer ,RideLocationSerializer


class RideViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()

    # choose serializer based on action
    def get_serializer_class(self):
        if self.action == "create":
            return RideCreateSerializer
        elif self.action == "retrieve":
            return RideDetailSerializer
        elif self.action in ["start", "complete", "cancel"]:
            return RideStatusSerializer
        elif self.action == "accept":
            return RideAcceptSerializer
        elif self.action == "location":
            return RideLocationSerializer
        return RideListSerializer

    # list rides of logged in user
    def list(self, request):
        rides = Ride.objects.filter(rider=request.user)

        page = self.paginate_queryset(rides)
        if page is not None:
            serializer = RideListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RideListSerializer(rides, many=True)
        return Response(serializer.data)

    # create ride
    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

    # -----------------------------
    # START RIDE
    # -----------------------------
    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        ride = self.get_object()

        if ride.status != "REQUESTED":
            return Response(
                {"error": "Ride cannot be started"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.status = "STARTED"
        ride.save()

        serializer = RideStatusSerializer(ride)
        return Response(serializer.data)

    # -----------------------------
    # COMPLETE RIDE
    # -----------------------------
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        ride = self.get_object()

        if ride.status != "STARTED":
            return Response(
                {"error": "Ride cannot be completed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.status = "COMPLETED"
        ride.save()

        serializer = RideStatusSerializer(ride)
        return Response(serializer.data)

    # -----------------------------
    # CANCEL RIDE
    # -----------------------------
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        ride = self.get_object()

        if ride.status != "REQUESTED":
            return Response(
                {"error": "Ride cannot be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.status = "CANCELLED"
        ride.save()

        serializer = RideStatusSerializer(ride)
        return Response(serializer.data)

    # -----------------------------
    # DRIVER ACCEPT RIDE
    # -----------------------------
    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        ride = self.get_object()

        if ride.status != "REQUESTED":
            return Response(
                {"error": "Ride cannot be accepted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ride.driver is not None:
            return Response(
                {"error": "Ride already has a driver"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.driver = request.user
        ride.save()

        serializer = RideAcceptSerializer(ride)
        return Response(serializer.data)
    
    # -----------------------------
    # RIDE LOCATION UPDATE / VIEW
    # -----------------------------
    @action(detail=True, methods=["get", "post"])
    def location(self, request, pk=None):
        ride = self.get_object()

        if request.method == "POST":
            serializer = RideLocationSerializer(ride, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = RideLocationSerializer(ride)
        return Response(serializer.data)

