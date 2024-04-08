from django.urls import path
from .views import InsuranceProviderSignupAPIView, InsuranceProviderProfileAPIView, InsurancePlanListCreateAPIView, InsurancePlanRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('signup/', InsuranceProviderSignupAPIView.as_view(), name='insurance-provider-signup'),
    path('profile/', InsuranceProviderProfileAPIView.as_view(), name='insurance-provider-profile'),
    path('plans/', InsurancePlanListCreateAPIView.as_view(), name='insurance-plan-list-create'),
    path('plans/<int:pk>/', InsurancePlanRetrieveUpdateDestroyAPIView.as_view(), name='insurance-plan-detail'),
]
