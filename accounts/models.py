from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    ('analyst', 'Data Analyst'),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    doctor_license = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    hospital_name = models.CharField(max_length=150, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username
