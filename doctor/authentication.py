from django.contrib.auth.backends import BaseBackend
from .models import Doctor
import logging

logger = logging.getLogger(__name__)

class DoctorAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            doctor = Doctor.objects.get(email=email)
            if doctor.check_password(password):
                return doctor
        except Doctor.DoesNotExist:
            logger.warning("Doctor with email %s does not exist", email)
            return None

    def get_user(self, user_id):
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            return None

