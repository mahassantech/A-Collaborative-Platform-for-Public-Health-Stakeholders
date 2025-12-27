from django.shortcuts import render
from subscriptions.models import SubscriptionPlan

def HomeView(request):
    plans = SubscriptionPlan.objects.all()
    return render(request,'base.html',{"plans": plans})