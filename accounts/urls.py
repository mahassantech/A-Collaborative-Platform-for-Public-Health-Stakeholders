from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="signup"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile_view, name="profile"),

    # Dashboards
    path("dashboard/patient/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("dashboard/analyst/", views.analyst_dashboard, name="analyst_dashboard"),
]
