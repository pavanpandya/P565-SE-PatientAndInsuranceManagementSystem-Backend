from .views import registrationView, CustomAuthToken, insuranceCompanyProfileView, patientHistoryView
from django.urls import path


app_name='insurance_provider'
urlpatterns = [
    path('registration/', registrationView.as_view(), name='api_patient_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_patient_login'),
    path('profile/', insuranceCompanyProfileView.as_view(), name='api_patient_profile'),
    path('history/:uuid/', patientHistoryView.as_view(), name='api_patient_history'),
]