
from django.urls import path
from . import views

urlpatterns = [
    path('insuranceProvider', views.insurance_provider, name='insurance_provider'),
    path('createInsurancePackage', views.create_insurance_package, name='create_insurance_package'),
    path('suggestInsurance/<str:token>/<str:insurance_id>', views.suggest_insurance, name='suggest_insurance'),
    path('suggestInsurancePatient/<str:token>/<str:insurance_pack>', views.suggest_insurance_patient, name='suggest_insurance_patient'),
]
