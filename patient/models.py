from django.db import models
from doctor.models import Doctor
from insurance_provider.models import InsuranceProvider
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import check_password
import uuid


class Patient(AbstractBaseUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    blood_group_type = models.CharField(max_length=10, default='unknown')
    mobile = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'date_of_birth', 'gender', 'mobile']


class PatientAppointment(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # hospital = models.ForeignKey('doctor.Hospital', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason = models.TextField()
    symptoms = models.TextField()
    admitted_or_not = models.BooleanField()

    @property
    def hospital_address(self):
        return self.doctor.hospital.hospital_address


class PatientTreatmentCost(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_charge = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2)
    other_charge = models.DecimalField(max_digits=10, decimal_places=2)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)


class OTPVerification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)