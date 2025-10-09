# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import ROLE_CHOICES

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return f"{self.username} ({self.role})"
