from django import forms
from django.core.validators import RegexValidator
from .models import Contact


class ContactForm(forms.ModelForm):
    # Phone number validator
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'address', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'id': 'email'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'id': 'address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'id': 'phone'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'id': 'subject'
            }, choices=[
                ('', 'Choose an option'),
                ('Business Strategy', 'Business Strategy'),
                ('Customer Experience', 'Customer Experience'),
                ('Sustainability and ESG', 'Sustainability and ESG'),
                ('Training and Development', 'Training and Development'),
                ('IT Support & Maintenance', 'IT Support & Maintenance'),
                ('Marketing Strategy', 'Marketing Strategy'),
            ]),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
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
        self.fields['phone'].validators.append(self.phone_validator)

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
        # Remove common formatting characters
        cleaned_phone = phone.replace(' ', '').replace(
            '-', '').replace('(', '').replace(')', '')

        if len(cleaned_phone) < 10:
            raise forms.ValidationError(
                'Phone number must be at least 10 digits.')
        if len(cleaned_phone) > 15:
            raise forms.ValidationError(
                'Phone number cannot be more than 15 digits.')

        return phone

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject or subject == '':
            raise forms.ValidationError('Please select a subject.')
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
