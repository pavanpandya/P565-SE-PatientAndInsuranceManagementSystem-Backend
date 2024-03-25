from django.db import models
from django.db.models.fields import DateField
from common.models import User



# Create your models here.
class doctor(models.Model):
    department=models.CharField(max_length=100)
    address= models.TextField()
    mobile=models.CharField(max_length=20)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
    






    