from rest_framework import serializers
from .models import InsuranceProvider, InsurancePlan

class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = ['id', 'company_name', 'address', 'mobile', 'email']
        read_only_fields = ['id']

class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = '__all__'
