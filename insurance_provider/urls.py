from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.InsuranceProviderSignupAPIView.as_view(), name='insurance_provider_signup'),
    path('login/', views.InsuranceProviderLoginAPIView.as_view(), name='insurance_provider_login'),
    path('activate/', views.InsuranceProviderVerifySignupOTPAPIView.as_view(), name='insurance_provider_verify_signup_otp'),
    path('verify/', views.InsuranceProviderVerifyLoginOTPAPIView.as_view(), name='insurance_provider_verify_login_otp'),
    path('profile/', views.InsuranceProviderProfileRetrieveAPIView.as_view(), name='insurance_provider_profile'),
    path('plans/', views.InsuranceProviderPlansAPIView.as_view(), name='insurance_provider_plans'),
    path('plans/create/', views.InsuranceProviderPlansAPIView.as_view(), name='insurance_provider_plans_create'),
    path('plans/<int:plan_id>/', views.InsuranceProviderPlansAPIView.as_view(), name='insurance_provider_plans_detail'),
]
