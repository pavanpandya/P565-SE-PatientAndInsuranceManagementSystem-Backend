import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Doctor(AbstractBaseUser):
    from hospital.models import Hospital
    specialty_choices = [
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Endocrinologist', 'Endocrinologist'),
        ('Gastroenterologist', 'Gastroenterologist'),
        ('Hematologist', 'Hematologist'),
        ('Nephrologist', 'Nephrologist'),
        ('Neurologist', 'Neurologist'),
        ('Oncologist', 'Oncologist'),
        ('Ophthalmologist', 'Ophthalmologist'),
        ('Orthopedic Surgeon', 'Orthopedic Surgeon'),
        ('Otolaryngologist', 'Otolaryngologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Physiatrist', 'Physiatrist'),
        ('Plastic Surgeon', 'Plastic Surgeon'),
        ('Podiatrist', 'Podiatrist'),
        ('Psychiatrist', 'Psychiatrist'),
        ('Pulmonologist', 'Pulmonologist'),
        ('Radiologist', 'Radiologist'),
        ('Rheumatologist', 'Rheumatologist'),
        ('Urologist', 'Urologist'),
        ('General Practitioner', 'General Practitioner'),
        ('Surgeon', 'Surgeon'),
        ('Anesthesiologist', 'Anesthesiologist'),
        ('Dentist', 'Dentist'),
        ('Dietitian', 'Dietitian'),
        ('Gynecologist', 'Gynecologist'),
        ('Physician', 'Physician'),
        ('Therapist', 'Therapist'),
        ('Other', 'Other')
    ]

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    licence_number = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, choices=specialty_choices)
    mobile = models.CharField(max_length=15)
    # date_of_birth = models.DateField()
    # gender = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'licence_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'specialty', 'mobile', 'hospital']

class DoctorSchedule(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=10)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)


class OTPVerification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)