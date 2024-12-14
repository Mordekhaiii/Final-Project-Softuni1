from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='products/', default='path/to/default/image.jpg')  # Default image path
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Update availability based on stock
        self.is_available = self.stock > 0
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def update_total_price(self):
        # Recalculate the total price from associated order items
        self.total_price = sum(item.quantity * item.price for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Update product stock on item save
        if self.pk is None:  # Check if item is new
            self.product.stock -= self.quantity
        else:
            # Adjust stock if quantity changes
            previous = OrderItem.objects.get(pk=self.pk)
            self.product.stock += previous.quantity - self.quantity
        self.product.save()
        super().save(*args, **kwargs)
