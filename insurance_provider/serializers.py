from rest_framework import serializers
from common.models import User
from django.contrib.auth.models import Group
from insurance_provider.models import InsuranceCompany, InsurancePlan  # Importing the new model

class InsuranceCompanyRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email:')
    company_name = serializers.CharField(label='Company Name:')
    password = serializers.CharField(label='Password:', style={'input_type': 'password'}, write_only=True, min_length=8, help_text="Your password must contain at least 8 characters and should not be entirely numeric.")
    confirm_password = serializers.CharField(label='Confirm password:', style={'input_type': 'password'}, write_only=True)

    def validate_email(self, email):
        email_exists = User.objects.filter(email__iexact=email)
        if email_exists:
            raise serializers.ValidationError({'email': 'This email address is already in use'})
        return email
    
    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'password must match'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            company_name=validated_data['company_name'],
            status=False
        )
        user.set_password(validated_data['password'])
        user.save()
        group_insurance_provider, created = Group.objects.get_or_create(name='InsuranceCompany')
        group_insurance_provider.user_set.add(user)
        return user
    

class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = ['id', 'plan_name', 'plan_description', 'plan_cost', 'includes_dental', 'includes_vision', 'includes_prescriptions']


class InsuranceCompanyProfileSerializer(serializers.ModelSerializer):

    mobile = serializers.CharField(label="Mobile Number:", max_length=20)
    address = serializers.CharField(label="Address:")
    insurance_plans = InsurancePlanSerializer(many=True)

    def validate_mobile(self, mobile):
        if not mobile.isdigit():
            raise serializers.ValidationError('Your mobile number should contain only numbers!')
        return mobile
    
    def create(self, validated_data):
        insurance_plans_data = validated_data.pop('insurance_plans')
        new_insurance_provider = InsuranceCompany.objects.create(
            mobile=validated_data['mobile'],
            address=validated_data['address'],
            user=validated_data['user']
        )
        for plan_data in insurance_plans_data:
            InsurancePlan.objects.create(company=new_insurance_provider, **plan_data)
        return new_insurance_provider
    
    def update(self, instance, validated_data):
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        # Update insurance plans
        insurance_plans_data = validated_data.get('insurance_plans', [])
        for plan_data in insurance_plans_data:
            plan_id = plan_data.get('id')
            if plan_id:
                plan = InsurancePlan.objects.get(id=plan_id, company=instance)
                plan.plan_name = plan_data.get('plan_name', plan.plan_name)
                plan.plan_description = plan_data.get('plan_description', plan.plan_description)
                plan.plan_cost = plan_data.get('plan_cost', plan.plan_cost)
                plan.includes_dental = plan_data.get('includes_dental', plan.includes_dental)
                plan.includes_vision = plan_data.get('includes_vision', plan.includes_vision)
                plan.includes_prescriptions = plan_data.get('includes_prescriptions', plan.includes_prescriptions)
                plan.save()
            else:
                InsurancePlan.objects.create(company=instance, **plan_data)
        return instance
    

class PatientHistorySerializerInsuranceCompanyView(serializers.ModelSerializer):
    admit_date = serializers.DateField(label='Admit Date:', read_only=True)
    release_date = serializers.DateField(label='Release Date:', required=False)
    patient = serializers.CharField(label='Patient:')
    assigned_doctor = serializers.CharField(label='Assigned Doctor:')
    department = serializers.CharField(label='Department:')
    symptomps=serializers.CharField(label="Symptoms:", style={'base_template': 'textarea.html'})

