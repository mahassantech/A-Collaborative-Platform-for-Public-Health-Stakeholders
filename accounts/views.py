from django.shortcuts import render
from .forms import SignUpForm

# Create your views here.
def SignUp(request):
    form=SignUpForm()
    return render(request,'accounts/signup.html',{'form':form})

def SignIn(request):
    return render(request,'accounts/signin.html')