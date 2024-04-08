from django.db import models

class InsuranceProvider(models.Model):
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    

class InsurancePlan(models.Model):
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255)
    plan_description = models.TextField()
    plan_cost = models.DecimalField(max_digits=10, decimal_places=2)
    includes_vision = models.BooleanField(default=False)
    includes_dental = models.BooleanField(default=False)
    includes_prescription = models.BooleanField(default=False)
