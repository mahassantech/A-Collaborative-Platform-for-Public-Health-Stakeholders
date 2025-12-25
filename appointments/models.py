# models.py
from django.conf import settings
from django.db import models
from accounts.models import CustomUser


class DoctorLocation(models.Model):
    APPOINTMENT_TYPE = (
        ("offline", "Offline"),
        ("online", "Online"),
        ("both", "Online & Offline"),
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_locations"
    )

    name = models.CharField(max_length=150)
    address = models.TextField()
    days = models.CharField(max_length=100, help_text="Sun,Tue,Thu")
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE)

    def allowed_days(self):
        return [d.strip().lower() for d in self.days.split(",")]

    def __str__(self):
        return self.name


APPOINTMENT_STATUS = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]


class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="doctor_appointments")
    location = models.ForeignKey(DoctorLocation, on_delete=models.CASCADE)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default="pending")
    notes = models.TextField(blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ("doctor", "location", "date", "start_time")

    def __str__(self):
        return f"{self.patient} {self.date} {self.start_time}"
