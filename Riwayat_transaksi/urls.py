from django.urls import path
from . import views

urlpatterns = [
    path('complete-order/', views.complete_order, name='complete_order'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    
]