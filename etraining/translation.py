from modeltranslation.translator import register, TranslationOptions
from .models import ECategory, ETrainingVideo, ETrainingDocs

@register(ECategory)
class ECategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ETrainingVideo)
class ETrainingVideoTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ETrainingDocs)
class ETrainingDocsTranslationOptions(TranslationOptions):
    fields = ('title',)