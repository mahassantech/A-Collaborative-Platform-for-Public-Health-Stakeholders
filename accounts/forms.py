from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "role", "doctor_license", "specialization", "hospital_name"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            "username", 
            "email", 
            "password", 
            "role", 
            "doctor_license", 
            "specialization", 
            "hospital_name",
            "profile_pic"
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "role",
            "doctor_license",
            "specialization",
            "hospital_name",
            "profile_pic"
        ]