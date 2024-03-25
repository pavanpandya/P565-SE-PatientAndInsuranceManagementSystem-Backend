from django.db import models
from common.models import User
import uuid

class InsuranceCompany(models.Model):
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.company_name
    
    @property
    def get_email(self):
        return self.email
    
    @property
    def get_id(self):
        return self.id

class InsurancePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, related_name='insurance_plans')
    plan_name = models.CharField(max_length=100)
    plan_description = models.TextField()
    plan_cost = models.DecimalField(max_digits=10, decimal_places=2)
    includes_dental = models.BooleanField()
    includes_vision = models.BooleanField()
    includes_prescriptions = models.BooleanField()
