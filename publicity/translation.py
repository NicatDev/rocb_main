from modeltranslation.translator import register, TranslationOptions
from .models.model_cct_center import CCTCenter, CCT_Center_Image
from .models.model_newsletter import Newsletter, NewsletterItems
from .models.model_outreach_materials import Outreach, OutreachEmbed
from .models.model_surveys import Survey

@register(CCTCenter)
class CCTCenterTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(CCT_Center_Image)
class CCT_Center_ImageTranslationOptions(TranslationOptions):
    fields = ('alttag',)

# --- Newsletter ---
@register(Newsletter)
class NewsletterTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(NewsletterItems)
class NewsletterItemsTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Outreach)
class OutreachTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(OutreachEmbed)
class OutreachEmbedTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title',)