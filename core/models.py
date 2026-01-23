from django.db import models
from accounts.models import CustomUser
from category.models import Category  

class HealthHistory(models.Model):
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="health_histories",
        limit_choices_to={"role": "patient"}
    )

    assigned_doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_health_posts",
        limit_choices_to={"role": "doctor"},
        help_text="Private post: only assigned doctor can see"
    )

    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    photo = models.ImageField(
    upload_to="health_history_photos/",  # Automatically saved in MEDIA_ROOT/health_history_photos/
    blank=True,
    null=True,
    help_text="Upload any image from your computer"
)

    treatment_taken = models.TextField(blank=True)

    is_private = models.BooleanField(
        default=True,
        help_text="Private = only patient + assigned doctor can see"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.patient.token_id})"
