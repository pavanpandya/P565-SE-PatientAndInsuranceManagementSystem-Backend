from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Doctor, OTPVerification

class DoctorSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'licence_number', 'specialty', 'mobile', 'hospital', 'password', 'confirm_password', 'is_verified']

    def validate(self, data):
        # Validate required fields are present
        required_fields = ['first_name', 'last_name', 'email', 'licence_number', 'specialty', 'mobile', 'hospital', 'password', 'confirm_password']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"The field '{field}' is missing. Please provide all the required fields.")

        # Validate password confirmation
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        
        # Check for unique email
        if Doctor.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email already exists.")

        return data

    def create(self, validated_data):
        # Remove confirm_password as it is not needed
        validated_data.pop('confirm_password', None)

        # Hash the password
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Create doctor instance
        doctor = super().create(validated_data)
        return doctor
    

class DoctorLoginSerializer(serializers.Serializer):
    licence_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Validate required fields
        licence_number = data.get('licence_number')
        password = data.get('password')

        if not licence_number:
            raise serializers.ValidationError("The licence_number field is required.")
        if not password:
            raise serializers.ValidationError("The password field is required.")

        # Return the validated data
        return data
    

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'licence_number', 'specialty', 'mobile', 'hospital', 'is_verified']
