from django.urls import path
from . import views
from .views import decrease_quantity
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('payment/', views.payment_list, name='payment_list'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('payment/<int:payment_id>/decrease/', decrease_quantity, name='decrease_quantity'),
    path('payment-order/', views.payment_order, name='payment_order'),
    path('add-to-payment/<int:product_id>/', views.add_to_payment, name='add_to_payment'),
    path('upload_payment_proof/<int:payment_id>/', views.upload_payment_proof, name='upload_payment_proof'),
]