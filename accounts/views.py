from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def SignUp(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=SignUpForm()
    return render(request,'accounts/signup.html',{'form':form})

def SignIn(request):
    form=AuthenticationForm()
    return render(request,'accounts/signin.html',{'form':form})