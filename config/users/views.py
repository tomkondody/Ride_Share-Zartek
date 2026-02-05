from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


class RegisterViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
