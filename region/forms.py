from django import forms
from django.forms import inlineformset_factory

from .models import AdditionalInformation, Country


class CountryOwnerForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = (
            'description_en',
            'description_ru',
            'href',
        )
        widgets = {
            'description_en': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'description_ru': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'href': forms.URLInput(attrs={'class': 'form-control'}),
        }


class AdditionalInformationOwnerForm(forms.ModelForm):
    class Meta:
        model = AdditionalInformation
        fields = (
            'key_en',
            'key_ru',
            'value_en',
            'value_ru',
            'order',
        )
        widgets = {
            'key_en': forms.TextInput(attrs={'class': 'form-control'}),
            'key_ru': forms.TextInput(attrs={'class': 'form-control'}),
            'value_en': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'value_ru': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


AdditionalInformationFormSet = inlineformset_factory(
    Country,
    AdditionalInformation,
    form=AdditionalInformationOwnerForm,
    extra=1,
    can_delete=True,
)
