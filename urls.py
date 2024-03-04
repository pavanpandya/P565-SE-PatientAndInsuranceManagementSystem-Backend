# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('doctor/', views.doctor_utility, name='doctor_utility'),
    path('patient/', views.patient_utility, name='patient_utility'),
    path('insurance_provider/', views.insurance_provider_utility, name='insurance_provider_utility'),
    path('common/', views.common_utility, name='common_utility'),
]
