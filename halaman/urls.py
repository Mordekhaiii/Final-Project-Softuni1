from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('home.html',views.home,name='home'),
    path('login/', views.loginPage, name='login'),
    path('register',views.registerPage,name='register'),
    path('profile/', views.profilePage, name='profile'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/edit/', views.edit_user_profile, name='edit_profile'),
    path('contact/', views.contact, name='contact'),
    path('profile/update_profile', views.update_user_profile, name='update_profile'),


]