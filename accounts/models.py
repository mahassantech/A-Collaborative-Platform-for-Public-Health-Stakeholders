import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import SPECIALIZATION_CHOICES, ROLE_CHOICES

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'
    )

    doctor_license = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # Multiple specializations allowed
    specialization = models.ManyToManyField(
        'Specialization',
        blank=True,
        help_text="Only for doctors"
    )

    hospital_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    profile_pic = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    # 🆔 UNIQUE TOKEN
    token_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    def __str__(self):
        return f"{self.username} | Token: {self.token_id}"


# আলাদা মডেল Specialization হিসেবে
class Specialization(models.Model):
    name = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES, unique=True)

    def __str__(self):
        return self.name
