import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import SPECIALIZATION_CHOICES, ROLE_CHOICES


# 🔹 Base62 encoder
BASE62 = string.digits + string.ascii_letters  # 0-9a-zA-Z

def encode_base62(num):
    if num == 0:
        return BASE62[0]
    base = len(BASE62)
    encoded = ""
    while num:
        num, rem = divmod(num, base)
        encoded = BASE62[rem] + encoded
    return encoded


# 🔹 Role prefix map
ROLE_PREFIX = {
    "doctor": "DR",
    "patient": "PT",
    "analyst": "AN",
}


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="patient"
    )

    doctor_license = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    specialization = models.ManyToManyField(
        "Specialization",
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

    # 🆔 ROLE-BASED TOKEN (Padded & Scalable)
    token_id = models.CharField(
        max_length=12,   # Adjust for future growth
        unique=True,
        blank=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.token_id:
            prefix = ROLE_PREFIX.get(self.role, "US")
            short_code = encode_base62(self.id)

            # 🔹 Determine padding length for min 6 char total
            min_total_length = 6  # prefix + dash + code
            padding_needed = max(min_total_length - len(prefix) - 1, 0)
            short_code_padded = short_code.rjust(padding_needed, "0")

            self.token_id = f"{prefix}-{short_code_padded}"
            super().save(update_fields=["token_id"])

    def __str__(self):
        return f"{self.username} | {self.token_id}"


class Specialization(models.Model):
    name = models.CharField(
        max_length=100,
        choices=SPECIALIZATION_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.name
