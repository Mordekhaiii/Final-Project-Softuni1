from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
# from .models import Order



# Cekout
# Cekout
# from .models import Product, Order, OrderItem
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'img')
    search_fields = ('name',)


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'payment_button')
#     actions = ['mark_as_paid', 'process_payment']

#     def mark_as_paid(self, request, queryset):
#         queryset.update(status='Paid')
#         self.message_user(request, "Selected orders have been marked as paid.")

#     def process_payment(self, request, queryset):
#         # Simulate or perform payment logic
#         for order in queryset:
#             # Implement the real payment logic here
#             order.status = 'Paid'
#             order.save()
#         self.message_user(request, "Selected orders have been processed for payment.")

#     def payment_button(self, obj):
#         # This adds a "Process Payment" button for each order in the admin list view
#         return format_html(
#             '<a class="button" href="/admin/orders/order/{}/process_payment/">Process Payment</a>',
#             obj.id
#         )

#     process_payment.short_description = "Process payment for selected orders"
#     mark_as_paid.short_description = "Mark selected orders as paid"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('orders/<int:order_id>/process_payment/', self.admin_site.admin_view(self.process_payment_view)),
#         ]
#         return custom_urls + urls

#     def process_payment_view(self, request, order_id):
#         order = Order.objects.get(id=order_id)
#         if request.method == "POST":
#             # Simulate processing payment
#             order.status = 'Paid'
#             order.save()
#             return HttpResponse(f"Payment processed for order {order_id}")

#         return render(request, 'orders/process_payment.html', {'order': order})
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'quantity', 'price')
#     search_fields = ['product__name']