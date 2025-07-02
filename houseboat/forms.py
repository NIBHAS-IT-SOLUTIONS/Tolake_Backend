from django import forms
from .models import Booking, ContactInquiry, Houseboat, CATEGORY_CHOICES
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'name', 'email', 'address', 'phone', 'houseboat',
            'category', 'check_in', 'check_out', 'total_guests'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Your Address', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-control'}),
            'houseboat': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=CATEGORY_CHOICES, attrs={'class': 'form-control'}),
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_guests': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Total Guests', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in < timezone.now().date():
                self.add_error('check_in', 'Check-in date cannot be in the past.')
            if check_out <= check_in:
                self.add_error('check_out', 'Check-out date must be after check-in.')

        return cleaned_data


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Your Message', 'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_str = str(phone)
        if not phone_str.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_str) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone
