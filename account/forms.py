from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile


class ChangePasswordForm(PasswordChangeForm):
    """Change password for the logged-in user (old + new + confirm)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_attrs = {
            'class': 'change-password-input',
            'autocomplete': 'off',
        }
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={**field_attrs, 'autocomplete': 'current-password', 'id': 'id_old_password'},
        )
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={**field_attrs, 'autocomplete': 'new-password', 'id': 'id_new_password1'},
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={**field_attrs, 'autocomplete': 'new-password', 'id': 'id_new_password2'},
        )
        self.fields['old_password'].label = _('Current password')
        self.fields['new_password1'].label = _('New password')
        self.fields['new_password2'].label = _('Confirm new password')


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control profile-input'}),
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control profile-input'}),
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control profile-input'}),
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control profile-input'}),
    )
    organization = forms.CharField(
        label=_('Organization'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control profile-input'}),
    )
    position = forms.CharField(
        label=_('Position'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control profile-input'}),
    )
    birth_date = forms.DateField(
        label=_('Date of birth'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control profile-input', 'type': 'date'}),
    )
    profile_picture = forms.ImageField(
        label=_('Profile picture'),
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

    def __init__(self, *args, user=None, profile=None, **kwargs):
        self.user = user
        self.profile = profile
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        if profile:
            self.fields['phone_number'].initial = profile.phone_number
            self.fields['organization'].initial = profile.organization
            self.fields['position'].initial = profile.position
            self.fields['birth_date'].initial = profile.birth_date

    def save(self):
        user = self.user
        profile = self.profile
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data['email']
        user.save()

        profile.phone_number = self.cleaned_data.get('phone_number') or None
        profile.organization = self.cleaned_data.get('organization') or None
        profile.position = self.cleaned_data.get('position') or None
        profile.birth_date = self.cleaned_data.get('birth_date') or None

        new_picture = self.cleaned_data.get('profile_picture')
        if new_picture:
            profile.profile_picture = new_picture

        profile.save()
        return profile
