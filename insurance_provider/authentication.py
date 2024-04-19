from django.contrib.auth.backends import BaseBackend
from .models import InsuranceProvider
import logging

logger = logging.getLogger(__name__)

class InsuranceProviderAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            insurance_provider = InsuranceProvider.objects.get(email=email)
            if insurance_provider.check_password(password):
                return insurance_provider
        except InsuranceProvider.DoesNotExist:
            logger.warning("InsuranceProvider with email %s does not exist", email)
            return None

    def get_user(self, user_id):
        try:
            return InsuranceProvider.objects.get(pk=user_id)
        except InsuranceProvider.DoesNotExist:
            return None
