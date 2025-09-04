from modeltranslation.translator import register, TranslationOptions
from .models import Profile 

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('organization', 'position')