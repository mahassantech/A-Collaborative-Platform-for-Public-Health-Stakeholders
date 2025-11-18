from django.shortcuts import render, redirect
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, "accounts/register_success.html", {"user": user})
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login(request):
    return render(request,'accounts/signin.html')