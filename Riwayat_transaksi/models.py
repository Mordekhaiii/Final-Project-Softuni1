from django.db import models
from django.contrib.auth.models import User
from orders.models import Product
from django.utils.timezone import now
from django.core.validators import MinValueValidator

class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Quantity must be at least 1")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price of the transaction")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Transaction by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
