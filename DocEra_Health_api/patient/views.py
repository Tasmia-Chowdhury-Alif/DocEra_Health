from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from . import serializers
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema


class IsPatientOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

# Create your views here.
@extend_schema(
    summary="List or manage patient profiles",
    description="Allows authenticated users to view or manage patient profiles. Non-admin users can only access their own profile."
)
class PatientViewset(viewsets.ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer
    permission_classes = [IsAuthenticated, IsPatientOrAdmin]

    # only admin users can access all patient objects. others can only access their own object
    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Patient.objects.all()
        return models.Patient.objects.filter(user=self.request.user)

# TODO : account activation using email
class PatientRegistrationView(UserViewSet):
    serializer_class = serializers.PatientRegistrationSerializer
    permission_classes = []

    @extend_schema(
        summary="Register a new patient",
        description="Creates a new patient with associated user account and returns JWT access and refresh tokens.",
        request=serializers.PatientRegistrationSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string", "description": "JWT refresh token"},
                    "access": {"type": "string", "description": "JWT access token"},
                },
            },
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        user = patient.user

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
