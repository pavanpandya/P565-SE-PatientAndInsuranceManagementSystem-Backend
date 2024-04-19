from django.db import models
from django.db.models import Count


class Hospital(models.Model):
    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital_name = models.CharField(max_length=255)
    hospital_address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    no_of_beds_available = models.IntegerField(default=0)

    def calculate_stats(self):
        from doctor.models import Doctor
        from patient.models import PatientAppointment
        # Calculate the number of doctors associated with this hospital
        no_of_doctors = Doctor.objects.filter(hospital=self).count()

        # Calculate the number of patients admitted to this hospital
        no_of_patient_admitted = PatientAppointment.objects.filter(
            hospital=self,
            admitted_or_not=True
        ).count()

        # Calculate the number of beds available in the hospital
        # by subtracting the number of admitted patients from the total beds available
        available_beds = self.no_of_beds_available - no_of_patient_admitted

        # Return the calculated statistics
        return {
            'no_of_doctors': no_of_doctors,
            'no_of_patient_admitted': no_of_patient_admitted,
            'no_of_beds_available': available_beds
        }
