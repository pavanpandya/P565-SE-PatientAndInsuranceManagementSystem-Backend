from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.HospitalRegistrationAPIView.as_view(), name='hospital_register'),
    path('all/', views.HospitalListAPIView.as_view(), name='hospital_list'),
    path('<int:hospital_id>/update/', views.HospitalUpdateAPIView.as_view(), name='hospital_update'),
]
