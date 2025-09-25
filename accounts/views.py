from django.shortcuts import render,redirect
from .forms import CustomUserCreationSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm


class SignUpView(CreateView):
    template_name='accounts/signup.html'
    form_class=CustomUserCreationSignUpForm
    success_url=reverse_lazy('login')

class SignInView(LoginView):
    template_name='accounts/signin.html'
    authentication_form = CustomAuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('profile')