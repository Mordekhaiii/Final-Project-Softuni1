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
    # Ambil semua payment terkait pengguna
    payments = Payment.objects.filter(user=request.user)

    if payments.exists():
        try:
            with transaction.atomic():  # Pastikan semua operasi dilakukan secara atomik
                for payment in payments:
                    # Pindahkan data ke TransactionHistory
                    TransactionHistory.objects.create(
                        date=payment.date,
                        user=payment.user,
                        perfume=payment.product,  # Pastikan field sesuai model TransactionHistory
                        quantity=payment.quantity,
                        total_price=payment.total_price,
                    )

                    # Hapus data dari Payment setelah disimpan di TransactionHistory
                    payment.delete()

                # Tambahkan pesan sukses
                messages.success(request, "Payment completed and moved to transaction history.")
        except Exception as e:
            # Jika ada error, tampilkan pesan dan kembali ke halaman payment_list
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('payment_list')

    # Redirect ke halaman riwayat transaksi setelah berhasil
    return redirect('transaction_history')


@login_required
def transaction_history(request):
    transactions = TransactionHistory.objects.filter(user=request.user).order_by('-id')
    return render(request, 'riwayat_transaksi/transaction_history.html', {'transactions': transactions})