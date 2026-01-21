from django.shortcuts import render,redirect
from .forms import HealthHistoryForm
from django.contrib.auth.decorators import login_required
from .models import HealthHistory
from django.http import HttpResponseForbidden
from django.db.models import Q  # doctor view filter: public OR assigned


# Create your views here.
def BlogPage(request):
    return render(request, "core/blog.html")

def CommunityPage(request):
    return render(request, "core/community.html")

def MyHealth(request):
    return render(request, "core/myhealth.html")

@login_required
def add_health_history(request):
    if request.user.role != "patient":
        return HttpResponseForbidden("Only patients can add health history")

    if request.method == "POST":
        # 🩺 Important: include request.FILES for ImageField
        form = HealthHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.patient = request.user
            post.save()
            form.save_m2m()  # In case you have ManyToMany fields like assigned_doctor.specialization
            return redirect("health_history_list")
    else:
        form = HealthHistoryForm()

    return render(request, "core/add.html", {"form": form})


@login_required
def health_history_list(request):
    if request.user.role == "patient":
        posts = HealthHistory.objects.filter(patient=request.user)
    elif request.user.role == "doctor":
        posts = HealthHistory.objects.filter(
            Q(is_private=False) | Q(assigned_doctor=request.user)
        )
    else:
        posts = HealthHistory.objects.none()

    return render(request, "core/myhealth.html", {"posts": posts})


def HealthPage(request):
    return render(request, "core/health.html")

def ConditionsPage(request):
    return render(request,'core/conditions.html')