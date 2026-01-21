from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/category/<slug:category_slug>/', views.blog_list, name='blog_by_category'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path("notifications/", views.notifications, name="notifications"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
