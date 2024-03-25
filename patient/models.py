from django.db import models
from common.models import User, Gender, BloodType
from doctor.models import doctor
from insurance_provider.models import InsuranceCompany


# Create your models here.
class patient(models.Model):
    mobile=models.CharField(max_length=20)
    age= models.DecimalField(max_digits=4,decimal_places=1)
    address= models.TextField()
    gender=models.CharField(choices=Gender.choices, max_length=6)
    blood_type=models.CharField(choices=BloodType.choices, max_length=3)
    insurance_provider=models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, default=None)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_email(self):
        return self.user.email
    
    @property
    def get_id(self):
        return self.user.id


class patient_history(models.Model):
    assigned_doctor=models.ForeignKey(doctor, on_delete=models.CASCADE)
    department=models.CharField(max_length=100)
    admit_date=models.DateField(verbose_name="Admit Date",auto_now=False, auto_now_add=True)
    symptomps=models.TextField()
    release_date=models.DateField(verbose_name="Release Date",auto_now=False, auto_now_add=False, null=True, blank=True)
    patient=models.ForeignKey(patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.get_name
    

class Appointment(models.Model):
    appointment_date=models.DateField(verbose_name="Appointment date",auto_now=False, auto_now_add=False)
    appointment_time=models.TimeField(verbose_name="Appointement time", auto_now=False, auto_now_add=False)
    status=models.BooleanField(default=False)
    patient_history=models.ForeignKey(patient_history,related_name='patient_appointments', on_delete=models.CASCADE)
    hospital_name=models.CharField(verbose_name="Hospital Name", max_length=100, null=False)
    doctor=models.ForeignKey(doctor,related_name='doctor_appointments',null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.patient_history.patient.get_name+'-'+self.doctor.get_name
    
    @property
    def patient_name(self):
        self.patient_history.patient.get_name
    

class patient_cost(models.Model):
    room_charge=models.PositiveIntegerField(verbose_name="Room charge", null=False)
    medicine_cost=models.PositiveIntegerField(verbose_name="Medicine cost", null=False)
    doctor_fee=models.PositiveIntegerField(verbose_name="Doctor Fee", null=False)
    other_charge=models.PositiveIntegerField(verbose_name="Other charges", null=False)
    patient_details=models.OneToOneField(patient_history, related_name='costs', on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return "{} tk" .format(self.room_charge+self.medicine_cost+self.doctor_fee+self.other_charge)
    

    def __str__(self):
        return self.patient_details.patient.get_name+'-'+str(self.patient_details.admit_date)