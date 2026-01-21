from django import forms
from .models import HealthHistory
from accounts.models import CustomUser
from category.models import Category

class HealthHistoryForm(forms.ModelForm):
    class Meta:
        model = HealthHistory
        fields = [
            "title",
            "category",
            "photo",
            "treatment_taken",
            "is_private",
            "assigned_doctor",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter health history title"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "treatment_taken": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe treatments taken"}),
            "is_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "assigned_doctor": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🩺 Assigned doctor dropdown: শুধু doctor দেখাবে, specializationসহ
        doctors = CustomUser.objects.filter(role="doctor")
        self.fields["assigned_doctor"].queryset = doctors
        self.fields["assigned_doctor"].required = False
        self.fields["assigned_doctor"].empty_label = "Select a doctor (optional)"
        self.fields["assigned_doctor"].label_from_instance = lambda obj: (
    f"Dr. {obj.first_name} {obj.last_name}" + 
    (f" — {', '.join([spec.name for spec in obj.specialization.all()])}" if obj.specialization.exists() else " — General")
)


        # 🏷️ Category dropdown
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].required = False
        self.fields["category"].empty_label = "Select your category"
