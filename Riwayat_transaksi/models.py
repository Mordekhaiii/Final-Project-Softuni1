from django.db import models
from django.contrib.auth.models import User
from orders.models import Product  # Updated to Product model
from django.utils.timezone import now

class TransactionHistory(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('QRIS', 'QRIS'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash'
    )
    payment_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    proof_of_payment = models.ImageField(
        upload_to='payment_proofs/', blank=True, null=True, help_text="Upload proof for QRIS payments only."
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        # Validasi bukti pembayaran jika metode adalah QRIS
        if self.payment_method == 'QRIS' and not self.proof_of_payment:
            raise ValidationError("Proof of payment is required for QRIS method.")
        if self.payment_method == 'Cash' and self.proof_of_payment:
            raise ValidationError("Proof of payment is not allowed for Cash method.")

    def __str__(self):
        return f"Transaction by {self.user.username} on {self.date}"
