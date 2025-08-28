from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from patient.views import PatientRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^auth/', include('djoser.urls')),  # /auth/users/, /auth/users/me/
    re_path(r'^auth/', include('djoser.urls.jwt')),  # /auth/jwt/create/, etc.

    path('auth/patients/register/', PatientRegistrationView.as_view({'post': 'create'}), name='patient-register'),

    path('contact_us/', include('contact_us.urls')),
    path('service/', include('service.urls')),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('appointment/', include('appointment.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
