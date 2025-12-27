import uuid
import requests
from .models import SubscriptionPlan
from django.shortcuts import render, get_object_or_404, redirect
from .models import SubscriptionPlan
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from subscriptions.utils import can_book_appointment  
from django.utils import timezone                      
from dateutil.relativedelta import relativedelta       
from .models import UserSubscription 
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentTransaction


def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, "subscriptions/plans.html", {"plans": plans})


def payment_page(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    return render(request, "subscriptions/payment.html", {"plan": plan})


@login_required
def sslcommerz_payment(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    tran_id = str(uuid.uuid4())

    # ✅ CREATE transaction (MUST)
    PaymentTransaction.objects.create(
        user=request.user,
        plan=plan,
        tran_id=tran_id,
        amount=plan.price,
        status="PENDING"
    )

    data = {
        "store_id": settings.SSLCOMMERZ_STORE_ID,
        "store_passwd": settings.SSLCOMMERZ_STORE_PASS,
        "total_amount": plan.price,
        "currency": "BDT",
        "tran_id": tran_id,

        "success_url": request.build_absolute_uri(reverse("payment_success")),
        "fail_url": request.build_absolute_uri(reverse("payment_fail")),
        "cancel_url": request.build_absolute_uri(reverse("payment_cancel")),

        "cus_name": request.user.username,
        "cus_email": request.user.email or "test@email.com",
        "cus_phone": "01700000000",
        "cus_add1": "Dhaka",
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",

        "shipping_method": "NO",
        "product_name": plan.get_name_display(),
        "product_category": "Subscription",
        "product_profile": "non-physical-goods",
    }

    response = requests.post(
        "https://sandbox.sslcommerz.com/gwprocess/v4/api.php",
        data=data
    )

    result = response.json()

    if result.get("status") == "SUCCESS":
        return redirect(result["GatewayPageURL"])

    messages.error(request, "Payment initialization failed")
    return redirect("subscription_plans")



@csrf_exempt
def payment_success(request):
    tran_id = request.POST.get("tran_id")

    # Transaction get or 404
    txn = get_object_or_404(PaymentTransaction, tran_id=tran_id)

    # Update transaction status if not already SUCCESS
    if txn.status != "SUCCESS":
        txn.status = "SUCCESS"
        txn.save()

        # Get or create subscription with defaults to avoid IntegrityError
        sub, created = UserSubscription.objects.get_or_create(
            user=txn.user,
            defaults={
                "start_date": timezone.now(),
                "end_date": timezone.now() + relativedelta(months=txn.plan.duration_months),
                "plan": txn.plan,
                "is_active": True
            }
        )

        # If subscription already existed, just activate/update it
        if not created:
            sub.activate_plan(txn.plan)

    # Redirect user to success page
    return redirect("payment_success_page")


@login_required
def payment_success_page(request):
    return render(request, "subscriptions/success.html")

@csrf_exempt
def payment_fail(request):
    tran_id = request.POST.get("tran_id")
    PaymentTransaction.objects.filter(tran_id=tran_id).update(status="FAILED")
    return redirect("payment_failed_page")


@csrf_exempt
def payment_cancel(request):
    tran_id = request.POST.get("tran_id")
    PaymentTransaction.objects.filter(tran_id=tran_id).update(status="CANCELLED")
    return redirect("payment_cancelled_page")

