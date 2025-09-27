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

# def add_author(request):
#     if request.method=="POST":
#         author_form=forms.AuthorForm(request.POST)
#         if author_form.is_valid():
#             author_form.save()
#             return redirect("add_author") #atar mane jeidata input dibo seta r fill a autofill thkbe na,ai data ta form a store hbe
#     else:
#         author_form=forms.AuthorForm()
#     return render(request,'add_author.html',{'form':author_form})