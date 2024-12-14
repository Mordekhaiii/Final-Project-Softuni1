from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment, Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from .forms import PaymentForm  # Impor PaymentForm
from .models import Product, Payment
from orders.models import Order


from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment

@login_required
def decrease_quantity(request, payment_id):
    # Dapatkan instance pembayaran
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    # Kurangi kuantitas jika > 1, jika tidak hapus
    if payment.quantity > 1:
        payment.quantity -= 1
        payment.save()
    else:
        payment.delete()

    # Redirect kembali ke halaman Payment List
    return redirect('payment_list')


from django.shortcuts import get_object_or_404, redirect
from .models import Payment
@login_required
@require_POST
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.delete()
    return redirect('payment_list')  # Adjust to the appropriate redirect



from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Product, Order, OrderItem

@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user)
    total_payment = sum(payment.total_price for payment in payments)
    return render(request, 'payment/payment_list.html', {
        'payments': payments,
        'total_payment': total_payment,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from orders.models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def payment_order(request, order_id):
    try:
        # Get the product from the database
        product = get_object_or_404(Product, id=order_id)

        # Ensure only one pending order exists for the user
        orders = Order.objects.filter(user=request.user, status='pending')
        if orders.exists():
            order = orders.first()  # Get the first order if multiple exist
            if orders.count() > 1:
                # Remove duplicates and keep only one
                orders.exclude(id=order.id).delete()
        else:
            # Create a new order if none exists
            order = Order.objects.create(user=request.user, status='pending')

        # Get the quantity from the query parameters (default to 1)
        quantity = int(request.GET.get('quantity', 1))

        # Check stock availability
        if product.stock < quantity:
            return JsonResponse({
                'status': 'error',
                'message': 'Not enough stock available'
            }, status=400)

        # Check if the product is already in the order
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        if not created:
            # If it already exists, update the quantity
            order_item.quantity += quantity
            order_item.save()

        # Update the product stock
        product.stock -= quantity
        product.save()

        # Redirect to the payment page
        return redirect('payment_order', product_id=product.id)  # Ganti 'payment:checkout' dengan nama URL Anda

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error adding product to order: {str(e)}'
        }, status=500)

# Add to payment
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment, Product

@login_required
def add_to_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Periksa apakah stok tersedia
    if product.stock <= 0:
        # Tambahkan pesan error jika stok tidak tersedia
        messages.error(request, f"Produk {product.name} sudah habis!")
        return redirect('product_list')

    # Tambahkan produk ke Payment List
    payment, created = Payment.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        # Jika sudah ada, tambahkan kuantitas
        payment.quantity += 1
        payment.save()

    return redirect('payment_list')
