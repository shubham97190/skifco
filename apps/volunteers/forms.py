from django import forms

from .models import Volunteer


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'city', 'interests', 'skills', 'availability', 'message', 'consent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'interests': forms.CheckboxSelectMultiple(),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your skills', 'rows': 3}),
            'availability': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Weekends, Evenings'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us more', 'rows': 3}),
            'consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError('You must agree to continue.')
        return consent
