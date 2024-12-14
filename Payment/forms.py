from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['product', 'quantity', 'payment_method']  # Hanya field yang dapat diedit
        labels = {
            'product': 'Product Name',
            'quantity': 'Quantity',
            'payment_method': 'Payment Method',
        }

    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        # Customizing the appearance of fields
        self.fields['product'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Perfume'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Quantity'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Payment Method'})
