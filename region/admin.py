from django.contrib import admin
from .models import (
    Region, RegionSection, MiniTitle, Image, BlockQuote, Tag,
    ListSection, ListItem, Country, ListSectionFile, AdditionalInformation,
)
from modeltranslation.admin import (
    TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline
) 

class MiniTitleInline(TranslationTabularInline):
    model = MiniTitle
    extra = 1

class ImageInline(TranslationTabularInline):
    model = Image
    extra = 1

class BlockQuoteInline(TranslationTabularInline):
    model = BlockQuote
    extra = 1

class RegionSectionInline(TranslationStackedInline):
    model = RegionSection
    extra = 1
    show_change_link = True

class ListItemInline(TranslationTabularInline):
    model = ListItem
    extra = 1

class ListSectionInline(TranslationStackedInline):
    model = ListSection
    extra = 1
    show_change_link = True

class TagInline(TranslationTabularInline):
    model = Tag
    extra = 1


@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    inlines = [TagInline, RegionSectionInline, ListSectionInline]


@admin.register(RegionSection)
class RegionSectionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "region", "order")
    list_filter = ("region",)
    search_fields = ("title", "description")
    ordering = ("order",)
    inlines = [MiniTitleInline, ImageInline, BlockQuoteInline]

class ListSectionFileInline(TranslationTabularInline):
    model = ListSectionFile
    extra = 1

@admin.register(ListSection)
class ListSectionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "region")
    search_fields = ("title", "description")
    list_filter = ("region",)
    inlines = [ListItemInline, ListSectionFileInline]


@admin.register(MiniTitle)
class MiniTitleAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'regionsection')

@admin.register(Image)
class ImageAdmin(TabbedTranslationAdmin):
    list_display = ('alttag', 'regionsection')

@admin.register(BlockQuote)
class BlockQuoteAdmin(TabbedTranslationAdmin):
    list_display = ('fullname', 'regionsection')

@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'region')

@admin.register(ListItem)
class ListItemAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'list_section')


class AdditionalInformationInline(TranslationTabularInline):
    model = AdditionalInformation
    extra = 1
    fields = ('key', 'value', 'order')


@admin.register(Country)
class CountryAdmin(TabbedTranslationAdmin):
    list_display = ("title", "region", "owner")
    search_fields = ("title", "description", "owner__username", "owner__email")
    list_filter = ("region",)
    autocomplete_fields = ('owner',)
    inlines = [AdditionalInformationInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'code', 'region', 'owner', 'flag_url', 'href'),
        }),
        ('Description', {
            'fields': ('description',),
        }),
    )


@admin.register(AdditionalInformation)
class AdditionalInformationAdmin(TabbedTranslationAdmin):
    list_display = ('country', 'key', 'order')
    list_filter = ('country__region', 'country')
    search_fields = ('key', 'value', 'country__title')