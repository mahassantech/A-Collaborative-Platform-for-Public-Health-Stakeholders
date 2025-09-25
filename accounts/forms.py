from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User   
from .constants import ROLE_CHOICES


class CustomUserCreationSignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
