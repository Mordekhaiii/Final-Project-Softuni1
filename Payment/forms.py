from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['product', 'quantity']  # 'payment_method' removed as it doesn't exist in the model.
        labels = {
            'product': 'Product Name',
            'quantity': 'Quantity',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizing the appearance of fields
        self.fields['product'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Product'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Quantity'})
