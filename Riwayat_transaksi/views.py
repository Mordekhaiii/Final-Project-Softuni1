from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import TransactionHistory
from Payment.models import Payment
from orders.models import Product  # Import Product model

@login_required
def complete_order(request):
    # Fetch payments for the logged-in user
    payments = Payment.objects.filter(user=request.user)

    if not payments.exists():
        messages.info(request, "No payments to process.")
        return redirect('transaction_history')

    try:
        with transaction.atomic():  # Ensure the transaction is atomic
            for payment in payments:
                print(f"Processing payment: {payment.id} for product: {payment.product.name} and user: {request.user.username}")

                # Create a TransactionHistory record for each payment
                transaction_history = TransactionHistory.objects.create(
                    user=request.user,
                    product=payment.product,  # Using product field
                    quantity=payment.quantity,
                    total_price=payment.total_price,
                    date=timezone.now(),
                    payment_method=payment.payment_method,  # Assuming this is present in Payment model
                )

                # Print or log the transaction created for debugging
                print(f"Transaction saved: {transaction_history}")

                # Delete the payment after saving it to transaction history
                payment.delete()

        messages.success(request, "All payments have been successfully moved to transaction history.")
    except Exception as e:
        print(f"Error occurred during transaction: {e}")
        messages.error(request, f"An error occurred: {e}")
        return redirect('payment_list')

    return redirect('transaction_history')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TransactionHistory

@login_required
def transaction_history(request):
    # Fetch transaction history for the logged-in user, ordered by creation date
    transactions = TransactionHistory.objects.filter(user=request.user).order_by('-date')  # 'date' for sorting

    return render(request, 'riwayat_transaksi/transaction_history.html', {'transactions': transactions})
