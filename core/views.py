from django.shortcuts import render

# Create your views here.
def BlogPage(request):
    return render(request, "core/blog.html")

def CommunityPage(request):
    return render(request, "core/community.html")

def TreatmentsPage(request):
    return render(request, "core/treatment.html")

def HealthPage(request):
    return render(request, "core/health.html")