from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from blog.models import BlogPost, Comment, Prescription
from accounts.models import CustomUser

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email")  # username বা email
        password = request.POST.get("password")

        # Check if identifier is an email
        try:
            user_obj = CustomUser.objects.get(email=identifier)
            username = user_obj.username
        except CustomUser.DoesNotExist:
            username = identifier  # assume it's username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")  
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    recent_posts = user.posts.all().order_by('-created_at')[:5]  # recent blog posts
    recent_comments = Comment.objects.filter(user=user).order_by('-created_at')[:5]
    recent_prescriptions = Prescription.objects.filter(doctor=user).order_by('-created_at')[:5] if user.role == 'doctor' else []

    context = {
        'user': user,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, "accounts/profile.html", context)

@login_required
def patient_dashboard(request):
    return render(request, "dashboards/patient_dashboard.html")

@login_required
def doctor_dashboard(request):
    return render(request, "dashboards/doctor_dashboard.html")

@login_required
def analyst_dashboard(request):
    return render(request, "dashboards/analyst_dashboard.html")

