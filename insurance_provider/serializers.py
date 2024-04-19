from rest_framework import serializers
from .models import InsuranceProvider, InsurancePlan
from django.contrib.auth.hashers import make_password


class InsuranceProviderSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = InsuranceProvider
        fields = ['company_name', 'email', 'address', 'mobile', 'password', 'confirm_password']

    def validate(self, data):
        # Check required fields
        required_fields = ['company_name', 'email', 'address', 'mobile', 'password', 'confirm_password']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"The field '{field}' is missing. Please provide all the required fields.")
        
        # Check if password and confirm_password match
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")
        
        # Check if email is already taken
        if InsuranceProvider.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated data
        validated_data.pop('confirm_password', None)

        # Hash the password
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Create the insurance provider
        return super().create(validated_data)


class InsuranceProviderLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            raise serializers.ValidationError("Both email and password are required.")

        return data


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = ['id', 'company_name', 'email', 'address', 'mobile']


class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = ['id', 'plan_name', 'plan_description', 'plan_cost', 'includes_prescription', 'includes_dental', 'includes_vision']