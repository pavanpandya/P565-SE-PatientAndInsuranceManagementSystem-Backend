from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.DoctorSignupAPIView.as_view(), name='doctor-signup'),
    path('profile/', views.DoctorProfileAPIView.as_view(), name='doctor-profile'),
    path('list-create/', views.DoctorListCreateAPIView.as_view(), name='doctor-list-create'),
    path('<int:pk>/', views.DoctorRetrieveUpdateDestroyAPIView.as_view(), name='doctor-detail'),
    path('working-hours/', views.WorkingHourListCreateAPIView.as_view(), name='working-hours-list-create'),
    path('working-hours/<int:pk>/', views.WorkingHourRetrieveUpdateDestroyAPIView.as_view(), name='working-hours-detail'),
    path('availability/', views.DoctorAvailabilityListAPIView.as_view(), name='doctor-availability'),
]
