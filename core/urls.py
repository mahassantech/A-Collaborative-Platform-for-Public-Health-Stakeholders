from django.urls import path
from . import views

urlpatterns = [
    path('',views.BlogPage,name='blogpage'),
]
