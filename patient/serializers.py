from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, PatientHistory, PatientAppointment
from doctor.models import Doctor
from django.contrib.auth.hashers import make_password


User = get_user_model()

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['insurance_provider', 'is_verified']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_verified'] = False  # Set is_verified to False by default
        return super().create(validated_data)

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = '__all__'

class PatientAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAppointment
        fields = '__all__'

class PatientProfileSerializer(serializers.ModelSerializer):
    patient_history = PatientHistorySerializer(many=True, read_only=True)
    appointments = PatientAppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile', 'date_of_birth', 'address', 'gender', 'blood_type', 'insurance_provider', 'patient_history', 'appointments']

class DoctorSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'speciality', 'department', 'associated_with_hospital']

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        otp = data['otp']
        return data
    
class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)