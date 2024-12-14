from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django import forms
from .models import Order, OrderItem, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'img', 'stock']

    def clean_stock(self):
        # Validasi bahwa stok tidak boleh negatif
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status', 'payment_method', 'payment_status', 'paid_amount']

    def clean_paid_amount(self):
        # Validasi bahwa jumlah pembayaran tidak boleh negatif
        paid_amount = self.cleaned_data.get('paid_amount')
        if paid_amount is not None and paid_amount < 0:
            raise forms.ValidationError("Paid amount cannot be negative.")
        return paid_amount

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

    def clean_quantity(self):
        # Validasi bahwa jumlah tidak boleh melebihi stok produk
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        if product and quantity > product.stock:
            raise forms.ValidationError(f"Quantity exceeds available stock. Only {product.stock} left.")
        return quantity

    def save(self, commit=True):
        # Kurangi stok produk sesuai jumlah pemesanan
        instance = super().save(commit=False)
        if instance.pk is None:  # Item baru
            instance.product.stock -= instance.quantity
        else:
            # Jika item diupdate, hitung perubahan stok
            previous = OrderItem.objects.get(pk=instance.pk)
            instance.product.stock += previous.quantity - instance.quantity

        if instance.product.stock < 0:
            raise forms.ValidationError("Not enough stock available.")

        instance.product.save()
        if commit:
            instance.save()
        return instance
