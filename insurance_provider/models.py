from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser


class InsuranceProvider(AbstractBaseUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'address', 'mobile']

class InsurancePlan(models.Model):
    def validate_plan_cost(value):
        if value < 0:
            raise ValidationError("Plan cost must be positive")

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name="plans")
    plan_name = models.CharField(max_length=255)
    plan_description = models.TextField()
    plan_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_plan_cost])
    includes_prescription = models.BooleanField(default=False)
    includes_dental = models.BooleanField(default=False)
    includes_vision = models.BooleanField(default=False)


class OTPVerification(models.Model):
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)