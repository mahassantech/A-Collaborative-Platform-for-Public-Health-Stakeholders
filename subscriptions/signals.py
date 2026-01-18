from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from .models import UserSubscription

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_free_subscription(sender, instance, created, **kwargs):
    if created:
        UserSubscription.objects.create(
            user=instance,
            plan=None,
            start_date=timezone.now(),  # <-- change here
            end_date=timezone.now(),    # <-- change here
            is_active=False
        )
