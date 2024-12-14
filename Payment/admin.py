from django.contrib import admin
from .models import Payment

# Validasi jika model sudah didaftarkan
if not admin.site.is_registered(Payment):
    @admin.register(Payment)
    class PaymentAdmin(admin.ModelAdmin):
        list_display = ('user', 'product', 'quantity', 'total_price', 'date')
