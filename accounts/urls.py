from django.urls import path
from . import views


urlpatterns = [
    path('signup/',views.register,name='signup'),
    path('login/',views.user_login,name='login'),
    # path('profile/',SignInView.as_view(),name='profile'),
]
