from django.urls import path
from .views import PatientSignUpAPIView, PatientLoginAPIView, PatientLoginVerifyOTPView, PatientVerifyOTPView, PatientProfileRetrieveAPIView, PatientProfileUpdateAPIView, PatientAppointmentBookingAPIView

urlpatterns = [
    path('signup/', PatientSignUpAPIView.as_view(), name='patient-signup'),
    path('login/', PatientLoginAPIView.as_view(), name='patient-login'),
    path('activate/', PatientVerifyOTPView.as_view(), name='patient-verify-otp'),
    path('verify/', PatientLoginVerifyOTPView.as_view(), name="patient-login-verify-otp"),
    path('<int:patient_id>/', PatientProfileRetrieveAPIView.as_view(), name='patient-retrieve'),
    path('<int:patient_id>/update/', PatientProfileUpdateAPIView.as_view(), name='patient-update'),
    path('appointments/', PatientAppointmentBookingAPIView.as_view(), name='patient-appointments-create'),  
    path('appointments/<int:pk>/', PatientAppointmentBookingAPIView.as_view(), name='patient-appointments-update'),
]