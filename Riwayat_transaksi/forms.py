from django import forms
from .models import TransactionHistory

class TransactionHistoryForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('QRIS', 'QRIS'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    
    # Menambahkan pilihan metode pembayaran (Cash atau QRIS)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    payment_status = forms.ChoiceField(choices=PAYMENT_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = TransactionHistory
        fields = ['product', 'quantity', 'total_price', 'payment_method', 'payment_status']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
