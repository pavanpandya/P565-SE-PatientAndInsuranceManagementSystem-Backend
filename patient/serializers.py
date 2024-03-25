from rest_framework import serializers
from common.models import User, Gender, BloodType
from patient.models import patient, patient_history, Appointment
from django.contrib.auth.models import Group
from doctor.models import doctor
from insurance_provider.models import InsuranceCompany
from insurance_provider.serializers import InsuranceCompanyProfileSerializer, InsurancePlanSerializer
 
 
class patientRegistrationSerializer(serializers.Serializer):

    email=serializers.EmailField(label='Email:')
    first_name=serializers.CharField(label='First name:')
    last_name=serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='Password:',style={'input_type': 'password'}, write_only=True, min_length=8, help_text="Your password must contain at least 8 characters and should not be entirely numeric.")
    confirm_password=serializers.CharField(label='Confirm password:',style={'input_type': 'password'},  write_only=True)
    

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
        password=data.get('password')
        confirm_password=data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'password':'password must match'})
        return data


    def create(self, validated_data):
        user= User.objects.create(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                status=False
            )
        user.set_password(validated_data['password'])
        user.save()
        group_patient, created = Group.objects.get_or_create(name='patient')
        group_patient.user_set.add(user)
        return user


class patientProfileSerializer(serializers.Serializer):
    mobile = serializers.CharField(label="Mobile Number:", max_length=20)
    age = serializers.DecimalField(label="Age:", max_digits=4, decimal_places=1)
    address = serializers.CharField(label="Address:")
    gender = serializers.ChoiceField(label='Gender:', choices=Gender.choices)
    blood_type = serializers.ChoiceField(label='Blood Type:', choices=BloodType.choices)
    insurance_provider = InsuranceCompanyProfileSerializer(required=False)

    def validate_mobile(self, mobile):
        if not mobile.isdigit():
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile

    def create(self, validated_data):
        if 'insurance_provider' in validated_data:
            insurance_provider_data = validated_data.pop('insurance_provider')
            insurance_provider = InsuranceCompany.objects.create(**insurance_provider_data)
        else:
            insurance_provider = None

        new_patient = patient.objects.create(
            mobile=validated_data['mobile'],
            age=validated_data['age'],
            address=validated_data['address'],
            gender=validated_data['gender'],
            blood_type=validated_data['blood_type'],
            insurance_provider=insurance_provider,
            user=validated_data['user']
        )
        return new_patient
    
    def update(self, instance, validated_data):
        instance.age=validated_data.get('age', instance.age)
        instance.address=validated_data.get('address', instance.address)
        instance.mobile=validated_data.get('mobile', instance.mobile)
        instance.gender=validated_data.get('gender', instance.gender)
        instance.blood_type=validated_data.get('blood_type', instance.blood_type)
        instance.insurance_provider=validated_data.get('insurance_provider', instance.insurance_provider)
        instance.save()
        return instance


class appointmentSerializerPatient(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    appointment_date = serializers.DateField(label='Appointment date')
    appointment_time = serializers.TimeField(label='Appointement time')
    status = serializers.BooleanField(required=False, read_only=True)
    hospital_name = serializers.CharField(label='Hospital Name:')
    doctor = serializers.PrimaryKeyRelatedField(queryset=doctor.objects.all(), required=False)


    def create(self, validated_data):
        new_appointment= Appointment.objects.create(
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            status=False,
            patient_history=validated_data['patient_history'],
            hospital_name=validated_data['hospital_name'],
            doctor=validated_data['doctor']
        )
        return new_appointment


class patientCostSerializer(serializers.Serializer):
    room_charge=serializers.IntegerField(label="Room Charge:")
    medicine_cost=serializers.IntegerField(label="Medicine Cost:")
    doctor_fee=serializers.IntegerField(label="Doctor Fee:")
    other_charge=serializers.IntegerField(label="Other Charge:")
    total_cost=serializers.CharField(label="Total Cost:")


class patientHistorySerializer(serializers.Serializer):
    #required=False; if this field is not required to be present during deserialization.
    admit_date=serializers.DateField(label="Admit Date:", read_only=True)
    symptomps=serializers.CharField(label="Symptomps:", style={'base_template': 'textarea.html'})
    department=serializers.CharField(label='Department:')
    release_date=serializers.DateField(label="Release Date:", required=False)
    assigned_doctor=serializers.StringRelatedField(label='Assigned Doctor:')
    patient_appointments=appointmentSerializerPatient(label="Appointments",many=True)
    costs=patientCostSerializer()