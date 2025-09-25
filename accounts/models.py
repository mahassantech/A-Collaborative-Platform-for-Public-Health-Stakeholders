from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import ROLE_CHOICES

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    token = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
