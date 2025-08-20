from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('list', views.PatientViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegistrationApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
]
