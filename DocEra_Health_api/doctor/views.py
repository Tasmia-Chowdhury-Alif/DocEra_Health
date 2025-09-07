from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.permissions import IsAdminOrReadOnly

# Create your views here.


class DoctorPagination(PageNumberPagination):
    page_size = 10  # items per page
    page_size_query_param = "page_size"
    max_page_size = 50


# this filter is used to get a doctor's all Available time and Reviews
class FilterByDoctorId(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id = request.query_params.get("doctor_id")
        if doctor_id:
            # the default reated name of Doctor model for AvailableTime model is doctor
            return queryset.filter(doctor__id=doctor_id)
        return queryset


class DoctorViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer
    pagination_class = DoctorPagination


class DesignationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Designation.objects.all()
    serializer_class = serializers.DesignationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']


class SpecializationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']


class AvailableTimeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.AvailableTime.objects.all()
    serializer_class = serializers.AvailableTimeSerializer
    filter_backends = [FilterByDoctorId]


class ReviewViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    filter_backends = [FilterByDoctorId]
