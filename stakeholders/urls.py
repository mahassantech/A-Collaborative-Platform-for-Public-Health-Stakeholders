from django.contrib import admin
from django.urls import path,include
from stakeholders import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeView,name='homes'),
    path('core/',include('core.urls')),
    path('',include('accounts.urls')),
    path("blog/", include("blog.urls")),

]
