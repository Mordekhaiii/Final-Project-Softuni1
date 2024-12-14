from django.urls import path
from . import views
from django.urls import path, include
from django.contrib import admin
from .views import product_list, product_create, update_stock, product_delete
from .views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home.html',views.home,name='home'),
    path('', views.user_orders_view, name='user_orders'),
    path('products/', views.product_list, name='product_list'),  # Display the products
    # Admin
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/<int:id>/edit/', views.product_edit, name='product_edit'),
    path('settings/', views.product_setting, name='product_setting'),
    path('update_stock/<int:pk>/', views.update_stock, name='update_stock'),
    path('orders/product_summary/<int:pk>/', views.product_summary, name='product_summary'),
    # End
    path('orders/details/<int:order_id>/', views.order_detail, name='order_detail'),

]
