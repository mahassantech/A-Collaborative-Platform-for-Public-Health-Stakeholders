from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="signup"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile_view, name="profile"),
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    
    path('doctor-dashboard/', views.doctor_dashboard, name='patient_lists'),
    path('patients/<int:patient_id>/', views.view_patient, name='view_patient'),
    path('patients/<int:patient_id>/export/csv/', views.export_patient_csv, name='export_patient_csv'),
    path('patients/<int:patient_id>/export/pdf/', views.export_patient_pdf, name='export_patient_pdf'),

    # Dashboards
    path("dashboard/patient/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("dashboard/analyst/", views.analyst_dashboard, name="analyst_dashboard"),
]
