from django.db import models
from accounts.models import User
from .constant import ROLE_CHOICES
import uuid

class Membership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
