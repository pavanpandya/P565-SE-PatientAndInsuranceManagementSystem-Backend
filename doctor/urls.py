from django.urls import path
from . import views

app_name = 'doctor_utility'

urlpatterns = [
    path('', views.index, name='index'),
    path('doctor/', views.doctor, name='doctor'),
    path('completeAppointment/<str:patientId>/', views.complete_appointment, name='complete_appointment'),
    path('markAsCompleteAppointment/<str:patientId>/', views.mark_as_complete_appointment, name='mark_as_complete_appointment'),
]
