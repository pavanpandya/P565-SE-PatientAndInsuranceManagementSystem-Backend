from django.urls import path
from .views import (
    PatientSignupAPIView,
    PatientProfileAPIView,
    DoctorSearchAPIView,
    PatientAppointmentCreateAPIView,
    PatientLoginAPIView,
    PatientVerifyOTPAPIView
)

urlpatterns = [
    path('signup/', PatientSignupAPIView.as_view(), name='patient-signup'),
    path('profile/', PatientProfileAPIView.as_view(), name='patient-profile'),
    path('search-doctors/', DoctorSearchAPIView.as_view(), name='doctor-search'),
    path('create-appointment/', PatientAppointmentCreateAPIView.as_view(), name='create-appointment'),
    path('login/', PatientLoginAPIView.as_view(), name='patient-login'),
    path('verify-otp/', PatientVerifyOTPAPIView.as_view(), name='verify-otp'),
]
