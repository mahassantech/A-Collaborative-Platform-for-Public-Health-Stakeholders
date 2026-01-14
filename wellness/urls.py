from django.urls import path
from . import views

urlpatterns = [
    path('', views.wellness_list, name='wellness_list'),
    path('create/', views.wellness_create, name='wellness_create'),
    path('<int:pk>/', views.wellness_detail, name='wellness_detail'),
    path('<int:pk>/edit/', views.wellness_edit, name='wellness_edit'),
    path('<int:pk>/delete/', views.wellness_delete, name='wellness_delete'),
]
