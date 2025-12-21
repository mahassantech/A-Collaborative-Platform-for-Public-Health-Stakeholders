import csv
import pdfkit  
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from .forms import RegistrationForm
from blog.models import Comment
from accounts.models import CustomUser
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import TokenRecoveryForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from .forms import TokenRecoveryForm
from .models import CustomUser
from django.conf import settings





# REGISTER VIEW

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)  # Include profile_pic
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
        else:
            print(form.errors)  # Debugging
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


# LOGIN VIEW

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email")  # Can be username or email
        password = request.POST.get("password")

        # Identify user by email or username
        try:
            user_obj = CustomUser.objects.get(email=identifier)
            username = user_obj.username
        except CustomUser.DoesNotExist:
            username = identifier  # Assume username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "accounts/login.html")

# LOGOUT VIEW

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# PROFILE VIEW

@login_required
def profile_view(request):
    user = request.user
    recent_posts = user.posts.all().order_by('-created_at')[:5]  # recent posts
    recent_comments = Comment.objects.filter(user=user).order_by('-created_at')[:5]
    context = {
        'user': user,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
    }
    return render(request, "accounts/profile.html", context)


# EDIT PROFILE VIEW

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            print(user_form.errors)  # Debugging

    else:
        user_form = UserUpdateForm(instance=user)

    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form
    })




# token views 

# Step 1: Token input & send email link
def token_recovery_view(request):
    if request.method == "POST":
        form = TokenRecoveryForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token_id"]
            user = CustomUser.objects.get(token_id=token)

            # Generate one-time reset token
            reset_token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse("token_reset_password_verify", args=[user.pk, reset_token])
            )

            # Send email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, "Password reset link has been sent to your registered email.")
            return redirect("token_recovery")
    else:
        form = TokenRecoveryForm()

    return render(request, "accounts/token_recovery.html", {"form": form})


# Step 2: Verify link & reset password
def token_reset_password_verify_view(request, uid, token):
    try:
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid link.")
        return redirect("token_recovery")

    if not default_token_generator.check_token(user, token):
        messages.error(request, "Link expired or invalid.")
        return redirect("token_recovery")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password reset successful. You can now login.")
            return redirect("login")
    else:
        form = SetPasswordForm(user)

    return render(request, "accounts/token_reset_password.html", {"form": form})



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
