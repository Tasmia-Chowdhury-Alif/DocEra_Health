from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()

router.register('', views.AppointmentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', views.AppointmentViewset.as_view({'post': 'stripe_webhook'}), name='stripe_webhook'),
]
