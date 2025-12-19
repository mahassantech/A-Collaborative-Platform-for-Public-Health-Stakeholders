from django import forms
from .models import CustomUser, Specialization

# REGISTRATION FORM
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    # Multi-select specialization
    specialization = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

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
            "profile_pic",
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")

        # Doctor validation
        if role == "doctor":
            if not cleaned_data.get("specialization"):
                self.add_error("specialization", "At least one specialization is required for doctors.")
            if not cleaned_data.get("doctor_license"):
                self.add_error("doctor_license", "Doctor license is required.")
            if not cleaned_data.get("hospital_name"):
                self.add_error("hospital_name", "Hospital name is required.")
        else:
            # Non-doctor cleanup
            cleaned_data["specialization"] = None
            cleaned_data["doctor_license"] = None
            cleaned_data["hospital_name"] = None

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Save ManyToManyField after initial save
            if self.cleaned_data.get("specialization"):
                user.specialization.set(self.cleaned_data["specialization"])
        return user


# PROFILE UPDATE FORM
class UserUpdateForm(forms.ModelForm):
    specialization = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "doctor_license",
            "specialization",
            "hospital_name",
            "profile_pic",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Email always read-only
        self.fields['email'].disabled = True

        if self.instance.role == 'doctor':
            # Doctor license read-only
            self.fields['doctor_license'].disabled = True
            # Specializations editable
            self.fields['specialization'].disabled = False
            # Hospital name editable
            self.fields['hospital_name'].disabled = False
        else:
            # Non-doctor → all doctor fields disabled
            self.fields['doctor_license'].disabled = True
            self.fields['specialization'].disabled = True
            self.fields['hospital_name'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.role != "doctor":
            # None assign না করে empty queryset / empty string assign করো
            cleaned_data["specialization"] = Specialization.objects.none()
            cleaned_data["doctor_license"] = ""
            cleaned_data["hospital_name"] = ""
        return cleaned_data


# token form added  

class TokenRecoveryForm(forms.Form):
    token_id = forms.CharField(
        max_length=12,
        label="Your Token ID",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your token"})
    )

    def clean_token_id(self):
        token = self.cleaned_data.get("token_id")
        if not CustomUser.objects.filter(token_id=token).exists():
            raise forms.ValidationError("Invalid token!")
        return token