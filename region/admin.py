from django.contrib import admin
from .models import (
    Region, RegionSection, MiniTitle, Image, BlockQuote, Tag,
    ListSection, ListItem, Country
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


# --- Main Admin classes updated for modeltranslation ---

@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "created_at", "created_by")
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


@admin.register(ListSection)
class ListSectionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "region")
    search_fields = ("title", "description")
    list_filter = ("region",)
    inlines = [ListItemInline]


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


@admin.register(Country)
class CountryAdmin(TabbedTranslationAdmin):
    list_display = ("title", "region")
    search_fields = ("title", "description")
    list_filter = ("region",)
    list_editable = ("region",)