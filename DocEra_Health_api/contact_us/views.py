from django.shortcuts import render
from rest_framework import viewsets
from . import models 
from . import serializers 

# Create your views here.
class ContactUsViewset(viewsets.ModelViewSet):
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer