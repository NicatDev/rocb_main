from modeltranslation.translator import register, TranslationOptions
from .models import Analytics, AnalyticsSection, Image 

@register(Analytics)
class AnalyticsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(AnalyticsSection)
class AnalyticsSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ('alttag',)