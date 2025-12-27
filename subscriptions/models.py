from django.db import models
from django.conf import settings  # CustomUser er jonno used
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # ensures CustomUser is used


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ("premium_6", "Premium 6 Months"),
        ("premium_12", "Premium 12 Months"),
    )

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.PositiveIntegerField()

    def __str__(self):
        return self.get_name_display()


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey('SubscriptionPlan', on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    is_active = models.BooleanField(default=False)

    def activate_plan(self, plan):
        self.plan = plan
        self.start_date = timezone.now()
        self.end_date = self.start_date + relativedelta(months=plan.duration_months)
        self.is_active = True
        self.save()

# transaction model for payment

class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    tran_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tran_id} - {self.status}"
