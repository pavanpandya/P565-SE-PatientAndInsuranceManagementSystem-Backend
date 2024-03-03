from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Patient(CustomUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    height = models.IntegerField()
    weight = models.IntegerField()
    current_medication = models.TextField()
    current_illness = models.TextField()
    allergies = models.TextField()
    emergency_contact_name = models.CharField(max_length=30)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_email = models.EmailField()
    insurance_provider = models.CharField(max_length=30)
    insurance_policy_number = models.CharField(max_length=20)
    insurance_group_number = models.CharField(max_length=20)
    contact_person_phone = models.CharField(max_length=15)
    contact_person_email = models.EmailField()

class Doctor(CustomUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    specialty = models.CharField(max_length=50)
    rating = models.IntegerField()
    degree = models.CharField(max_length=50)
    certificate_number = models.CharField(max_length=30)
    hospital = models.CharField(max_length=100)

class InsuranceProvider(CustomUser):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    website = models.URLField()
    price = models.IntegerField()
    package_name = models.CharField(max_length=30)
    package_description = models.TextField()
    insurance_duration = models.IntegerField()
    contact_person = models.CharField(max_length=30)
    contact_person_phone = models.CharField(max_length=15)
    contact_person_email = models.EmailField()
