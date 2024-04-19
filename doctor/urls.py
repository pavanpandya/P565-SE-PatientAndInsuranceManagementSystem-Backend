from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.DoctorSignupAPIView.as_view(), name='doctor_signup'),
    path('login/', views.DoctorLoginAPIView.as_view(), name='doctor_login'),
    path('activate/', views.DoctorVerifySignupOTPAPIView.as_view(), name='doctor_verify_signup_otp'),
    path('verify/', views.DoctorVerifyLoginOTPAPIView.as_view(), name='doctor_verify_login_otp'),
    path('<int:doctor_id>/profile/', views.DoctorProfileRetrieveAPIView.as_view(), name='doctor_profile'),
    # path('<int:doctor_id>/schedule/', views.DoctorScheduleAPIView.as_view(), name='doctor_schedule'),
]
