from django.db import models
from django.conf import settings
from orders.models import Product  # Pastikan model Product ada dan digunakan sebagai model produk

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('QRIS', 'QRIS'),
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
    date = models.DateTimeField(auto_now_add=True, verbose_name='Payment Date')

    def save(self, *args, **kwargs):
        # Hitung total harga berdasarkan harga produk dan jumlah
        if self.product and hasattr(self.product, 'price'):
            self.total_price = self.quantity * self.product.price
        else:
            self.total_price = 0.00
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Payments"
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.quantity} pcs - {self.payment_method}'


