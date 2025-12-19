from django.contrib import admin
from django.urls import path,include
from stakeholders import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeView,name='homes'),
    path('core/',include('core.urls')),
    path('accounts/',include('accounts.urls')),
    path("blog/", include("blog.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
