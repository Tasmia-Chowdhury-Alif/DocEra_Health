from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('list', views.DoctorViewset)
router.register('Designation', views.DesignationViewset)
router.register('Specialization', views.SpecializationViewset)
router.register('AvailableTime', views.AvailableTimeViewset)
router.register('Review', views.ReviewViewset)


urlpatterns = [
    path('', include(router.urls)),
]
