from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from Riwayat_transaksi.models import TransactionHistory
from orders.models import Product  # Import Product model
from Payment.models import Payment, PaymentProof
from django.contrib import messages
from .forms import PaymentProofForm

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


@login_required
def decrease_quantity(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)  # Pastikan hanya milik user ini
    product = payment.product

    # Pastikan stok dan quantity cukup
    if payment.quantity > 1:  # Pastikan quantity lebih dari 1 sebelum dikurangi
        try:
            with transaction.atomic():  # Gunakan transaksi untuk memastikan atomicity
                # Mengurangi stok produk sebanyak 1 unit
                product.stock += 1  # Kembalikan stok 1 unit
                product.save()

                # Mengurangi jumlah pembayaran sebanyak 1 unit
                payment.quantity -= 1
                payment.total_price = payment.quantity * product.price  # Hitung ulang total harga
                payment.save()

        except Exception as e:
            print(f"Error: {e}")
            pass  # Menangani exception jika ada error dalam pengurangan

    return redirect('payment_list')


# Payment List
@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user)
    total_payment = sum(payment.total_price for payment in payments)

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        form = PaymentProofForm(request.POST, request.FILES)

        if not payment_id:
            messages.error(request, "Invalid payment ID.")
            return redirect('payment_list')

        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Simpan bukti pembayaran
                    payment_proof = form.save(commit=False)
                    payment_proof.payment = payment
                    payment_proof.uploaded_at = timezone.now()
                    payment_proof.save()

                    # Ubah status pembayaran menjadi sukses
                    payment.status = 'success'
                    payment.proof = payment_proof.proof
                    payment.save()

                    messages.success(request, "Payment successfully updated to success.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

        else:
            messages.error(request, "Please provide a valid payment proof.")

        return redirect('payment_list')

    return render(request, 'payment/payment_list.html', {
        'payments': payments,
        'total_payment': total_payment,
        'form': PaymentProofForm(), 
    })


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
        payment.total_price = payment.quantity * product.price
        payment.save()

    return redirect('payment_list')


# Bukti Upload Pembayaran
from django.shortcuts import render, redirect
from .models import Payment

def upload_payment_proof(request, payment_id):
    # Handle the payment proof upload here
    payment = Payment.objects.get(id=payment_id)
    if request.method == 'POST' and request.FILES['proof']:
        payment.proof = request.FILES['proof']
        payment.save()
        return redirect('payment_list')  # Or any other redirect you prefer
    return render(request, 'payment/upload_proof.html', {'payment': payment})
