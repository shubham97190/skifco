from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['aid_type', 'details', 'requested_amount']
        widgets = {
            'aid_type': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your need'}),
            'requested_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount needed (optional)'}),
        }
