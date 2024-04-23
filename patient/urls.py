from django.urls import path
from .views import PatientSignUpAPIView, PatientLoginAPIView, PatientLoginVerifyOTPView, PatientVerifyOTPView, PatientForgotPasswordAPIView, PatientResetPasswordAPIView, PatientProfileRetrieveAPIView, PatientProfileUpdateAPIView, PatientAppointmentBookingAPIView, PatientReviewAPIView, DoctorSearchAPIView

urlpatterns = [
    path('signup/', PatientSignUpAPIView.as_view(), name='patient-signup'),
    path('login/', PatientLoginAPIView.as_view(), name='patient-login'),
    path('activate/', PatientVerifyOTPView.as_view(), name='patient-verify-otp'),
    path('verify/', PatientLoginVerifyOTPView.as_view(), name="patient-login-verify-otp"),
    path('forgot-password/', PatientForgotPasswordAPIView.as_view(), name='patient-forgot-password'),
    path('reset-password/verify/<str:uidb64>/<str:token>/', PatientResetPasswordAPIView.as_view(), name='patient-reset-password'),
    path('profile/', PatientProfileRetrieveAPIView.as_view(), name='patient-retrieve'),
    path('update/', PatientProfileUpdateAPIView.as_view(), name='patient-update'),
    path('appointments/', PatientAppointmentBookingAPIView.as_view(), name='patient-appointments-create-or-get-all'),  
    path('appointments/<int:pk>/', PatientAppointmentBookingAPIView.as_view(), name='patient-get-specific-appointment'),
    path('appointments/update/<int:pk>/', PatientAppointmentBookingAPIView.as_view(), name='patient-appointments-update'),
    path('appointments/reviews/', PatientReviewAPIView.as_view(), name='patient-reviews-get-all'),
    path('search-doctors/', DoctorSearchAPIView.as_view(), name='search-doctors'),
]