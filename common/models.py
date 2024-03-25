import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(_('first name'), max_length=150)
    status=models.BooleanField(default=False)


class Gender(models.TextChoices):
    FEMALE = "female",
    MALE = "male",
    OTHER = "other"


class BloodType(models.TextChoices):
    A_POSITIVE = "A+",
    A_NEGATIVE = "A-",
    B_POSITIVE = "B+",
    B_NEGATIVE = "B-",
    O_POSITIVE = "O+",
    O_NEGATIVE = "O-",
    AB_POSITIVE = "AB+",
    AB_NEGATIVE = "AB-",
    UNKNOWN = "UNK"
