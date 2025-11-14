from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('analyst', 'Analyst'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(16)  # auto token generate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
