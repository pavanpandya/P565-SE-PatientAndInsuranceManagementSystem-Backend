from patient.models import Appointment
from rest_framework import serializers
from common.models import User
from doctor.models import doctor
from django.contrib.auth.models import Group



class doctorRegistrationSerializer(serializers.Serializer):

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
        group_doctor, created = Group.objects.get_or_create(name='doctor')
        group_doctor.user_set.add(user)
        return user


class doctorProfileSerializer(serializers.Serializer):
    
    department=serializers.CharField(label='Department:')
    address= serializers.CharField(label="Address:")
    mobile=serializers.CharField(label="Mobile Number:", max_length=20)

    def validate_mobile(self, mobile):
        if mobile.isdigit()==False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile
    
    def create(self, validated_data):
        new_doctor= doctor.objects.create(
            department=validated_data['department'],
            address=validated_data['address'],
            mobile=validated_data['mobile'],
            user=validated_data['user']
        )
        return new_doctor
    
    def update(self, instance, validated_data):
        instance.department=validated_data.get('department', instance.department)
        instance.address=validated_data.get('address', instance.address)
        instance.mobile=validated_data.get('mobile', instance.mobile)
        instance.save()
        return instance


class patientHistorySerializerDoctorView(serializers.Serializer):
    #required=False; if this field is not required to be present during deserialization.
    admit_date=serializers.DateField(label="Admit Date:", read_only=True)
    symptomps=serializers.CharField(label="Symptomps:", style={'base_template': 'textarea.html'})
    department=serializers.CharField(label='Department:')
    release_date=serializers.DateField(label="Release Date:", required=False)
    assigned_doctor=serializers.StringRelatedField(label='Assigned Doctor:')
    

class doctorAppointmentSerializer(serializers.Serializer):
    patient_name=serializers.SerializerMethodField('related_patient_name')
    patient_age=serializers.SerializerMethodField('related_patient_age')
    appointment_date=serializers.DateField(label="Appointment Date:",)
    appointment_time=serializers.TimeField(label="Appointment Time:")
    patient_history=patientHistorySerializerDoctorView(label='patient History:')
    
    def related_patient_name(self, obj):
        return obj.patient_history.patient.get_name
    
    def related_patient_age(self, obj):
        return obj.patient_history.patient.age