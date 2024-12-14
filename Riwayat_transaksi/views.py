from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import TransactionHistory
from Payment.models import Payment
from .models import Product
from orders.models import Order


@login_required
def complete_order(request):
    payments = Payment.objects.filter(user=request.user)

    if payments.exists():
        try:
            with transaction.atomic():
                # Pindahkan data dari Payment ke TransactionHistory
                for payment in payments:
                    TransactionHistory.objects.create(
                        date=payment.date,
                        user=payment.user,
                        perfume=payment.product,
                        quantity=payment.quantity,
                        total_price=payment.total_price,
                    )

                    # Tambahkan logika untuk menghapus data di Payment
                    payment.delete()
        except Exception as e:
            return redirect('payment_list')  # Jika terjadi kesalahan, kembali ke daftar pembayaran

    return redirect('transaction_history')  # Alihkan ke halaman riwayat transaksi


@login_required
def transaction_history(request):
    transactions = TransactionHistory.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders/order_detail.html', {'transactions': transactions})