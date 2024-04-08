from django.db import models
from doctor.models import Doctor
from insurance_provider.models import InsuranceProvider

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=5)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, default='1')

class PatientHistory(models.Model):
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    admit_date = models.DateField()
    release_date = models.DateField()
    symptoms = models.TextField()

class PatientAppointment(models.Model):
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reason = models.TextField()

class PatientTreatmentCost(models.Model):
    room_charge = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_charge = models.DecimalField(max_digits=10, decimal_places=2)
    other_charge = models.DecimalField(max_digits=10, decimal_places=2)
    doctor_fee = models.DecimalField(max_digits=10, decimal_places=2)
    patient_details = models.ForeignKey(Patient, on_delete=models.CASCADE)
