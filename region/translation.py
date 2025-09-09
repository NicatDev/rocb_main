from modeltranslation.translator import register, TranslationOptions
from .models import (
    Region, RegionSection, MiniTitle, Image, BlockQuote, Tag,
    ListSection, ListItem, Country, ListSectionFile
)

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'author', 'position')

@register(RegionSection)
class RegionSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(MiniTitle)
class MiniTitleTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ('alttag',)

@register(BlockQuote)
class BlockQuoteTranslationOptions(TranslationOptions):
    fields = ('content',)

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ListSection)
class ListSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(ListItem)
class ListItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'code')

@register(ListSectionFile)
class ListSectionFileTranslationOptions(TranslationOptions):
    fields = ('file_name',)