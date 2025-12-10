from django.urls import path
from . import views

urlpatterns = [
    path('blog/',views.BlogPage,name='blogpage'),
    path('Community/',views.CommunityPage,name='CommunityPage'),
    path('treatments/',views.TreatmentsPage,name='treatmentPage'),
    path('myhealth/',views.HealthPage,name='healthPage'),
    path('conditons/',views.ConditionsPage,name='conditionspage'),
    
]
