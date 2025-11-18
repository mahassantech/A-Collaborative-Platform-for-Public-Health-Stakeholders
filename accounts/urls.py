from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.register_view, name='signup'),

    path('login/',views.login,name='login'),
    # path('profile/',SignInView.as_view(),name='profile'),
]
