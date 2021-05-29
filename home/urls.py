from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.signup,name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout')
]
