from rest_framework import serializers
from .models import Doctor, WorkingHour

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile', 'date_of_birth', 'licence_number', 'specialties', 'hospitals']
        read_only_fields = ['id']

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ['id', 'doctor', 'day_of_week', 'start_time', 'break_start_time', 'break_end_time', 'end_time', 'hospital']
        read_only_fields = ['id']