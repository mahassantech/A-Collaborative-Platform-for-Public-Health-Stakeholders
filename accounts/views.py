import csv
import pdfkit  
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from blog.models import BlogPost, Comment, Prescription
from accounts.models import CustomUser
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .models import CustomUser  # Custom user
from django.template.loader import render_to_string
from .forms import UserUpdateForm


# Doctor Dashboard: List of patients


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
        identifier = request.POST.get("email")  # username or email
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
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        # Include request.FILES for profile_pic
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            # Print errors to debug if save fails
            print(user_form.errors)

    else:
        user_form = UserUpdateForm(instance=user)

    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form
    })

@login_required
def patient_dashboard(request):
    return render(request, "dashboards/patient_dashboard.html")

@login_required
def doctor_dashboard(request):
    return render(request, "dashboards/doctor_dashboard.html")

@login_required
def analyst_dashboard(request):
    return render(request, "dashboards/analyst_dashboard.html")


# Doctor Dashboard - List all patients
@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Not authorized")
    
    patients = CustomUser.objects.filter(role='patient').order_by('-date_joined')
    return render(request, 'dashboards/doctor_dashboard.html', {'patients': patients})

# View Patient Details
@login_required
def view_patient(request, patient_id):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("Not authorized")

    patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
    
    # Posts, comments, prescriptions
    recent_posts = patient.posts.all().order_by('-created_at') if hasattr(patient, 'posts') else []
    recent_comments = patient.comments.all().order_by('-created_at') if hasattr(patient, 'comments') else []
    recent_prescriptions = patient.prescriptions.all().order_by('-created_at') if hasattr(patient, 'prescriptions') else []

    context = {
        'patient': patient,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, 'accounts/view_patient.html', context)

# Export CSV
@login_required
def export_patient_csv(request, patient_id):
    if request.user.role != 'doctor':
        return HttpResponseForbidden()
    patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{patient.username}_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Content', 'Created At'])
    for post in patient.posts.all():
        writer.writerow([post.title, post.content, post.created_at])
    return response

# Export PDF
@login_required
def export_patient_pdf(request, patient_id):
    if request.user.role != 'doctor':
        return HttpResponseForbidden()
    patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
    html = render_to_string('doctor/patient_pdf.html', {'patient': patient})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{patient.username}_data.pdf"'
    return response
