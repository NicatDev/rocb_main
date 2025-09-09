from modeltranslation.translator import register, TranslationOptions
from .models import About, AboutSection, MiniTitle, Image, Tag, ContactPoint

@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'description','author', 'position')

@register(AboutSection)
class AboutSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(MiniTitle)
class MiniTitleTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ('alttag',)

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ContactPoint)
class ContactPointTranslationOptions(TranslationOptions):
    fields = ('title',)