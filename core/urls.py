from django.urls import path
from . import views

urlpatterns = [
    path('blog/',views.BlogPage,name='blogpage'),
    path('Community/',views.CommunityPage,name='CommunityPage'),
    path('Community/',views.TreatmentsPage,name='treatmentPage'),
]
