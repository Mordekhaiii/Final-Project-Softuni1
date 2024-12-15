from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from orders.models import Product  # Pastikan model Product ada dan sudah sesuai kebutuhan

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('QRIS', 'QRIS'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_payments',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Price')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='Cash',
        verbose_name='Payment Method'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Payment Status'
    )
    proof = models.ImageField(
        upload_to='payment_proofs/',
        blank=True,
        null=True,
        verbose_name='Payment Proof'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Payment Date')

    def clean(self):
        # Validasi jumlah
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')
        super().clean()

    def save(self, *args, **kwargs):
        # Hitung total harga
        if self.product and hasattr(self.product, 'price'):
            self.total_price = self.quantity * self.product.price
        else:
            raise ValueError("The selected product does not have a valid price.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Payments"
        ordering = ['-date']

    def __str__(self):
        return f"Payment by {self.user.username} | {self.product.name} | Qty: {self.quantity} | Total: Rp{self.total_price} | {self.payment_method} | Status: {self.status}"


# Signals to handle stock changes
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Payment)
def reduce_stock_on_payment_save(sender, instance, **kwargs):
    instance.product.stock -= instance.quantity
    instance.product.save()

@receiver(post_delete, sender=Payment)
def restore_stock_on_payment_delete(sender, instance, **kwargs):
    instance.product.stock += instance.quantity
    instance.product.save()

class PaymentProof(models.Model):
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name='payment_proof',
        verbose_name='Payment'
    )
    proof = models.ImageField(
        upload_to='payment_proof/',
        verbose_name='Proof of Payment'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At')

    class Meta:
        verbose_name_plural = "Payment Proof"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Proof for Payment ID {self.payment.id}"
