from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.

class DoctorPagination(PageNumberPagination):
    page_size = 1 # items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000

class DoctorViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer
    pagination_class = DoctorPagination

class FilterByDoctorId(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get('doctor_id')
        if doctor_id :
            return queryset.filter(doctor= doctor_id)
        return queryset

class DesignationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Designation.objects.all()
    serializer_class = serializers.DesignationSerializer
    filter_backends = [FilterByDoctorId]

class SpecializationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    filter_backends = [FilterByDoctorId]

class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get("doctor_id")
        if doctor_id :
            return queryset.filter(doctor= doctor_id) # the default reated name of Doctor model for AvailableTime model is doctor
        return queryset

class AvailableTimeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.AvailableTime.objects.all()
    serializer_class = serializers.AvailableTimeSerializer
    filter_backends = [AvailableTimeForSpecificDoctor]


class ReviewViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    filter_backends = [FilterByDoctorId]
