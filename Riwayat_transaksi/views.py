from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from .models import TransactionHistory
from Payment.models import Payment


@login_required
def complete_order(request):
    """Handles payment completion and redirects to Transaction History."""
    if request.method == 'POST':
        # Ambil payment_method dari form
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('payment_list')

        # Ambil daftar pembayaran untuk user
        payments = Payment.objects.filter(user=request.user)

        if not payments.exists():
            messages.info(request, "No payments to process.")
            return redirect('payment_list')

        try:
            for payment in payments:
                # Jika metode pembayaran adalah QRIS
                if payment_method == 'QRIS':
                    proof = request.FILES.get('proof')
                    if not proof:
                        messages.error(request, "Proof of payment is required for QRIS.")
                        return redirect('payment_list')
                    
                    # Buat transaksi dengan status Pending
                    TransactionHistory.objects.create(
                        user=request.user,
                        product=payment.product,
                        quantity=payment.quantity,
                        total_price=payment.total_price,
                        date=timezone.now(),
                        payment_method=payment_method,
                        payment_status='Pending',  # Awalnya Pending
                        proof_of_payment=proof  # Simpan bukti pembayaran
                    )

                # Jika metode pembayaran adalah Cash
                elif payment_method == 'Cash':
                    TransactionHistory.objects.create(
                        user=request.user,
                        product=payment.product,
                        quantity=payment.quantity,
                        total_price=payment.total_price,
                        date=timezone.now(),
                        payment_method=payment_method,
                        payment_status='Completed',  # Langsung Completed
                    )

                # Hapus pembayaran dari daftar Payment setelah diproses
                payment.delete()

            messages.success(request, "Payment processed successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('payment_list')

        return redirect('transaction_history')


@login_required
def transaction_history(request):
    """Display the user's transaction history."""
    transactions = TransactionHistory.objects.filter(user=request.user).order_by('-date')

    for transaction in transactions:
        # Perbarui status pembayaran QRIS dari Pending ke Completed jika validasi diperlukan
        if (
            transaction.payment_method == 'QRIS' 
            and transaction.payment_status == 'Completed'
            and transaction.proof_of_payment
        ):
            transaction.payment_status = 'Completed'
            transaction.save()

    return render(
        request,
        'riwayat_transaksi/transaction_history.html',
        {'transactions': transactions}
    )
