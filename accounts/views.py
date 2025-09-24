from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy


class SignUpView(CreateView):
    template_name='accounts/signup.html'
    form_class=SignUpForm
    success_url=reverse_lazy('login')

class SignInView(LoginView):
    template_name='accounts/signin.html'
    
    def get_success_url(self):
        return reverse_lazy('profile')