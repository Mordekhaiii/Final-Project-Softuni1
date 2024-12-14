from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import TransactionHistory
from Payment.models import Payment
from .models import Product
from orders.models import Order
from django.contrib import messages

@login_required
def complete_order(request):
    payments = Payment.objects.filter(user=request.user)

    if not payments.exists():
        print("No payments found for the user.")
        messages.info(request, "No payments to process.")
        return redirect('transaction_history')

    try:
        with transaction.atomic():
            for payment in payments:
                print(f"Processing payment: {payment.id}, product: {payment.product.name}")
                # Tambahkan data ke TransactionHistory
                TransactionHistory.objects.create(
                    date=payment.date,
                    user=payment.user,
                    product=payment.product,  # Mengubah 'perfume' menjadi 'product'
                    quantity=payment.quantity,
                    total_price=payment.total_price,
                )
                print(f"Transaction saved for product: {payment.product.name}")
                # Hapus data di Payment
                payment.delete()
        messages.success(request, "All payments have been successfully moved to transaction history.")
    except Exception as e:
        print(f"Error occurred during transaction: {e}")
        messages.error(request, f"An error occurred: {e}")
        return redirect('payment_list')

    return redirect('transaction_history')





@login_required
def transaction_history(request):
    transactions = TransactionHistory.objects.filter(user=request.user).order_by('-id')
    return render(request, 'riwayat_transaksi/transaction_history.html', {'transactions': transactions})