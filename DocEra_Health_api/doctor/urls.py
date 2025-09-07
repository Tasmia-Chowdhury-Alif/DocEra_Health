from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('list', views.DoctorViewset)
router.register('designations', views.DesignationViewset)
router.register('specializations', views.SpecializationViewset)
router.register('available-times', views.AvailableTimeViewset)
router.register('reviews', views.ReviewViewset)


urlpatterns = [
    path('', include(router.urls)),
]
