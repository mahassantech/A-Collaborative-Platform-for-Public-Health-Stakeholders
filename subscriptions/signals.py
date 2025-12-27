from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserSubscription, SubscriptionPlan
from datetime import date

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_free_subscription(sender, instance, created, **kwargs):
    if created:
        # Free plan only for display, not active
        UserSubscription.objects.create(
            user=instance,
            plan=None,
            start_date=date.today(),
            end_date=date.today(),
            is_active=False
        )
