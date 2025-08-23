from django import forms
from django.core.validators import RegexValidator
from .models import Contact


class ContactForm(forms.ModelForm):
    # Phone number validator
    # phone_validator = RegexValidator(
    #     regex=r'^\+?\d{9,15}$',
    #     message="Phone number must contain 9 to 15 digits (optionally with +)."
    # )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'address', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '',
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': '',
                'id': 'email'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': '',
                'id': 'address'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '',
                'id': 'phone'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': '',
                'id': 'subject'
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': '',
                'id': 'message'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Field-ləri required et
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['subject'].required = True
        self.fields['message'].required = True
        self.fields['address'].required = False  # Address optional

        # Phone validator əlavə et
        # self.fields['phone'].validators.append(self.phone_validator)

        # Help texts
        self.fields['name'].help_text = 'Enter your full name'
        self.fields['email'].help_text = 'Enter a valid email address'
        self.fields['phone'].help_text = 'Enter your phone number'
        self.fields['message'].help_text = 'Minimum 10 characters required'

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError(
                'Name must be at least 2 characters long.')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'Name should only contain letters and spaces.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # yalnız rəqəmləri saxla
        cleaned_phone = ''.join(filter(str.isdigit, phone))

        if len(cleaned_phone) < 9:
            raise forms.ValidationError(
                'Phone number must be at least 9 digits.')
        if len(cleaned_phone) > 15:
            raise forms.ValidationError(
                'Phone number cannot be more than 15 digits.')

        return "+" + cleaned_phone if not phone.startswith("+") else phone

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if len(subject) < 2:
            raise forms.ValidationError(
                'Subject must be at least 2 characters long.')
        if not subject.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'Subject should only contain letters and spaces.')
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError(
                'Message must be at least 10 characters long.')
        if len(message) > 1000:
            raise forms.ValidationError(
                'Message cannot be more than 1000 characters long.')
        return message

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        return email
