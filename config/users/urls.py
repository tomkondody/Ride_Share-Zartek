from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
