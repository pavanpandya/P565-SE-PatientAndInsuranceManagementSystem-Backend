from django.contrib.auth.backends import BaseBackend
from .models import Patient
import logging

logger = logging.getLogger(__name__)

class PatientAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            patient = Patient.objects.get(email=email)
            if patient.check_password(password):
                return patient
        except Patient.DoesNotExist:
            logger.warning("Patient with email %s does not exist", email)
            return None

    def get_user(self, user_id):
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            return None
