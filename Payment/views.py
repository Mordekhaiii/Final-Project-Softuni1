from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from orders.models import Product  # Import Product model
from Payment.models import Payment

@login_required
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    try:
        with transaction.atomic():

            # Get the related product
            product = payment.product
            product.stock += payment.quantity  # Restore stock
            product.is_available = True  # Mark the product as available
            product.save()

            # Delete the payment
            payment.delete()

    except Exception as e:
        print(f"Error: {e}")
        pass  # Handle exception (if any)

    return redirect('payment_list')


from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from orders.models import Product  # Import Product model
from Payment.models import Payment

@login_required
def decrease_quantity(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    try:
        with transaction.atomic():
            if payment.quantity > 1:  # Ensure the quantity is greater than 1 before decreasing
                payment.quantity -= 1  # Decrease quantity
                payment.total_price = payment.quantity * payment.product.price  # Recalculate total price
                payment.save()

                # Get the related product
                product = payment.product
                product.stock += 1  # Restore stock by 1
                product.is_available = True  # Mark product as available
                product.save()

    except Exception as e:
        print(f"Error: {e}")
        pass  # Handle exception (if any)

    return redirect('payment_list')


@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user)
    total_payment = sum(payment.total_price for payment in payments)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, "Silakan pilih metode pembayaran")
            return redirect('payment_list')
            
        try:
            with transaction.atomic():
                for payment in payments:
                    # Buat record baru di TransactionHistory
                    TransactionHistory.objects.create(
                        user=payment.user,
                        product=payment.product,
                        quantity=payment.quantity,
                        total_price=payment.total_price,
                        payment_method=payment_method,
                        created_at=now()  # Menggunakan created_at dari model baru
                    )
                    # Hapus payment yang sudah diproses
                    payment.delete()
                
                messages.success(request, "Pembayaran berhasil dan telah ditambahkan ke riwayat transaksi.")
                return redirect('transaction_history')
                
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {e}")
    
    return render(request, 'payment/payment_list.html', {
        'payments': payments,
        'total_payment': total_payment,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from orders.models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required


@login_required
def payment_order(request, product_id):
    try:
        # Get the product from the database
        product = get_object_or_404(Product, id=product_id)

        # Get the quantity from the query parameters (default to 1)
        quantity = int(request.GET.get('quantity', 1))

        # Check stock availability
        if product.stock < quantity:
            messages.error(request, 'Not enough stock available')
            return redirect('product_list')

        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=quantity * product.price
        )

        # Update the product stock
        product.stock -= quantity
        product.save()

        return redirect('payment_list')

    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('product_list')
    
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
