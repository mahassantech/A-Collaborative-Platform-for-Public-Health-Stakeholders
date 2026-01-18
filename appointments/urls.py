from django.urls import path
from . import views

urlpatterns = [
    path("locations/", views.doctor_locations, name="doctor_locations"),
    path("locations/add/", views.add_location, name="add_location"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path('doctors/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),
    path('success/', views.appointments_success, name='appointments_success'),
    path('doctor/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor/appointments/', views.doctor_my_appointment, name='doctor_my_appointment'),
    
    path("doctor/appointments/", views.doctor_my_appointment, name="doctor_my_appointment"),
    path("patient/appointments/", views.my_appointments, name="my_appointments"),
    # path("analyst/appointments/", views.analyst_appointments, name="analyst_appointments"),
     
    
]
