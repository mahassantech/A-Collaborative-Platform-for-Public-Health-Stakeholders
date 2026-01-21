from django.shortcuts import render
from subscriptions.models import SubscriptionPlan
from blog.models import BlogPost

def HomeView(request):
    plans = SubscriptionPlan.objects.all()
    recent_blogs = BlogPost.objects.all().order_by('-created_at')[:3]  # latest 3 blogs
    return render(request, 'base.html', {
        "plans": plans,
        "recent_blogs": recent_blogs
    })