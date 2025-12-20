from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path("notifications/", views.notifications, name="notifications"),
]