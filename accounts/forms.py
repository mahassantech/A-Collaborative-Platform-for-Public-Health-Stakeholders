from django import forms

ROLE_CHOICES = [
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    ('analyst', 'Data Analyst'),
]

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    # Doctor-extra fields (MUST HAVE)
    doctor_license = forms.CharField(max_length=50, required=False)
    specialization = forms.CharField(max_length=100, required=False)
    hospital_name = forms.CharField(max_length=150, required=False)
