from rest_framework import serializers
from .models import Hospital

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'hospital_address', 'email', 'mobile', 'no_of_beds_available']

class HospitalCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'hospital_address', 'email', 'mobile', 'no_of_beds_available']

class HospitalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'hospital_address', 'email', 'mobile', 'no_of_beds_available']
