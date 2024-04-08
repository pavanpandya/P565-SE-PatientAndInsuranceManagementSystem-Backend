from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    num_bed_rooms = models.PositiveIntegerField()
    num_staff = models.PositiveIntegerField()
    num_doctors = models.PositiveIntegerField()

class Doctor(models.Model):
    SPECIALTIES = [
        ('General Physician', 'General Physician'),
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Neurologist', 'Neurologist'),
        ('Orthopedic Surgeon', 'Orthopedic Surgeon'),
        # Add more specialties as needed
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialties = models.CharField(max_length=100, choices=SPECIALTIES)
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    mobile = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    date_of_birth = models.DateField()
    licence_number = models.CharField(max_length=50, unique=True)
    hospitals = models.ManyToManyField(Hospital)  

class WorkingHour(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    break_start_time = models.TimeField(null=True, blank=True)
    break_end_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)