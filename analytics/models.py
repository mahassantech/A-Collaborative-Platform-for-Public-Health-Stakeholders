from django.conf import settings
from django.db import models

class Insight(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'analyst'}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
