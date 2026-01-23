from django.shortcuts import render,redirect
from .forms import HealthHistoryForm
from django.contrib.auth.decorators import login_required
from .models import HealthHistory
from django.http import HttpResponseForbidden
from django.db.models import Q 
from django.shortcuts import render, get_object_or_404


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
        form = HealthHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.patient = request.user

            # core logic
            if post.assigned_doctor:
                post.is_private = True   # doctor assigned → private
            else:
                post.is_private = False  # no doctor → public

            post.save()
            form.save_m2m()
            return redirect("health_history_list")
    else:
        form = HealthHistoryForm()

    return render(request, "core/add.html", {"form": form})

@login_required
def health_history_list(request):
    user = request.user

    # PUBLIC posts: no assigned doctor
    public_posts = HealthHistory.objects.filter(assigned_doctor__isnull=True)

    # PRIVATE posts: assigned doctor exists
    private_posts = HealthHistory.objects.filter(assigned_doctor__isnull=False)

    if user.role == "patient":
        posts = HealthHistory.objects.filter(
            Q(assigned_doctor__isnull=True) |   # public
            Q(patient=user)                     # own private
        )

    elif user.role == "doctor":
        posts = HealthHistory.objects.filter(
            Q(assigned_doctor__isnull=True) |   # public
            Q(assigned_doctor=user)              # assigned to this doctor
        )

    else:
        # analyst or others → only public
        posts = public_posts

    return render(request, "core/myhealth.html", {"posts": posts})

@login_required
def health_history_detail(request, pk):
    post = get_object_or_404(HealthHistory, pk=pk)
    user = request.user

    # 🔐 Access rules
    if post.assigned_doctor:
        if user != post.patient and user != post.assigned_doctor:
            return HttpResponseForbidden("You are not allowed to view this post.")
    # else: public (logged-in users only)

    return render(request, "core/health_detail.html", {"post": post})

def HealthPage(request):
    return render(request, "core/health.html")

def ConditionsPage(request):
    return render(request,'core/conditions.html')