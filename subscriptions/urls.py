from django.urls import path
from . import views

urlpatterns = [
    path("plans/", views.subscription_plans, name="subscription_plans"),
    path("payment/<int:plan_id>/", views.payment_page, name="payment_page"),
    path('payment/success-page/', views.payment_success_page, name='payment_success_page'),
    path("sslcommerz/<int:plan_id>/", views.sslcommerz_payment, name="sslcommerz_payment"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/fail/", views.payment_fail, name="payment_fail"),
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),
]
