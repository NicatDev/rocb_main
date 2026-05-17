from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

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
            'description_en': forms.Textarea(attrs={'rows': 5, 'class': 'form-control country-info-input'}),
            'description_ru': forms.Textarea(attrs={'rows': 5, 'class': 'form-control country-info-input'}),
            'href': forms.URLInput(attrs={'class': 'form-control country-info-input'}),
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
            'key_en': forms.TextInput(attrs={'class': 'form-control country-info-input'}),
            'key_ru': forms.TextInput(attrs={'class': 'form-control country-info-input'}),
            'value_en': forms.Textarea(attrs={'rows': 3, 'class': 'form-control country-info-input'}),
            'value_ru': forms.Textarea(attrs={'rows': 3, 'class': 'form-control country-info-input'}),
            'order': forms.HiddenInput(),
        }
        labels = {
            'key_en': _('Label'),
            'key_ru': _('Label'),
            'value_en': _('Information'),
            'value_ru': _('Information'),
        }


class BaseAdditionalInformationFormSet(forms.BaseInlineFormSet):
    def save(self, commit=True):
        instances = super().save(commit=False)
        for order, instance in enumerate(instances):
            instance.order = order
        if commit:
            for obj in self.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.save()
        return instances


AdditionalInformationFormSet = inlineformset_factory(
    Country,
    AdditionalInformation,
    form=AdditionalInformationOwnerForm,
    formset=BaseAdditionalInformationFormSet,
    extra=1,
    can_delete=True,
)
