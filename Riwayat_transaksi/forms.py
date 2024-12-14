from django import forms
from .models import TransactionHistory

class TransactionHistoryForm(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        fields = ['product', 'quantity', 'total_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }