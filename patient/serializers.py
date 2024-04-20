from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Patient, PatientAppointment, PatientReview
from django.utils import timezone


class PatientSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'address', 'date_of_birth', 'gender', 'blood_group_type', 'mobile', 'password', 'confirm_password']

    def validate(self, data):
        # Perform check if all fields are present
        required_fields = ['first_name', 'last_name', 'email', 'address', 'date_of_birth', 'gender', 'blood_group_type', 'mobile', 'password', 'confirm_password']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"The field '{field}' is missing. Please provide all the required fields.")
        
        # Perform check for password match
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match")
        
        # Perform check for unique email
        if Patient.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email already exists")
        
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated data
        validated_data.pop('confirm_password', None)

        # Hash the password
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Create the patient only after all validations are passed
        return super().create(validated_data)
    

class PatientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # Perform check if all fields are present
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("The email field is required.")
        if not password:
            raise serializers.ValidationError("The password field is required.")
        
        # Return the validated data
        return data


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'date_of_birth', 'gender', 'blood_group_type', 'mobile', 'is_verified']


class PatientAppointmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAppointment
        fields = ['id', 'appointment_date', 'appointment_time', 'doctor', 'patient', 'reason', 'symptoms', 'admitted_or_not', 'status']
        
    def validate(self, data):
        # Add custom validations here if needed.
        # For instance, you might want to check if the appointment_date is not in the past
        # Or if the doctor works at the hospital mentioned, etc.
        if data['appointment_date'] < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        
        if data['appointment_time'] < timezone.now().time() and data['appointment_date'] == timezone.now().date():
            raise serializers.ValidationError("Appointment time cannot be in the past.")
        
        # You can add more custom validations here as required.
        return data
    
    def create(self, validated_data):
        # Create the patient appointment only after all validations are passed
        return super().create(validated_data)
    

class PatientReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientReview
        fields = ['appointment', 'patient', 'doctor', 'rating', 'review']

        # validate function to check if the rating is between 1 and 5
        def validate(self, data):
            rating = data.get('rating')
            if rating < 1 or rating > 5:
                raise serializers.ValidationError("Rating must be between 1 and 5")
            
            return data
        
        def create(self, validated_data):
            # Create the patient review only after all validations are passed
            return super().create(validated_data)