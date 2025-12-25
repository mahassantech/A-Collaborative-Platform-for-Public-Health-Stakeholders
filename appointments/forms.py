from django import forms
from .models import DoctorLocation, Appointment

class DoctorLocationForm(forms.ModelForm):
    class Meta:
        model = DoctorLocation
        fields = [
            "name",
            "address",
            "days",
            "start_time",
            "end_time",
            "appointment_type",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "days": forms.TextInput(attrs={"class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "appointment_type": forms.Select(attrs={"class": "form-select"}),
        }


class AppointmentForm(forms.ModelForm):
    time_slot = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Appointment
        fields = ["location", "date", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }
