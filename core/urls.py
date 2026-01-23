from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('blog/',views.BlogPage,name='blogpage'),
    path('Community/',views.CommunityPage,name='CommunityPage'),
    path('myhealth/',views.MyHealth,name='myhealth'),
    # path('myhealth/',views.HealthPage,name='healthPage'),
    path('conditons/',views.ConditionsPage,name='conditionspage'),
    
    
    # share past storis
 
    path("", views.health_history_list, name="health_history_list"),
    path("add/", views.add_health_history, name="add_health_history"),
    path("health/<int:pk>/", views.health_history_detail, name="health_detail"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)