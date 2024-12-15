from django.urls import path
from . import views
from django.urls import path, include
from django.contrib import admin
from .views import product_list

urlpatterns = [
    # path('', views.user_orders_view, name='user_orders'),
    path('products/', views.product_list, name='product_list'),  # Display the products
    # Admin
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/<int:id>/edit/', views.product_edit, name='product_edit'),
    path('settings/', views.product_setting, name='product_setting'),
    # End
    # Profile
    path('profile/', views.profilePage, name='profile'),
    path('logout/', views.logoutUser, name='logout'),
    # End
      path('home.html',views.home,name='home'),
    path('home',views.home,name='home'),
    # path('orders/details/<int:order_id>/', views.order_detail, name='order_detail'),

]
