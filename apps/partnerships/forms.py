from django import forms

from .models import CSRInquiry


class CSRInquiryForm(forms.ModelForm):
    class Meta:
        model = CSRInquiry
        fields = ['org_name', 'contact_person', 'email', 'phone', 'csr_category', 'budget_range', 'message']
        widgets = {
            'org_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organisation Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'csr_category': forms.Select(attrs={'class': 'form-select'}),
            'budget_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Budget Range'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }
