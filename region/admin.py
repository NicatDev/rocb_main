from django.contrib import admin
from .models import (
    Region, RegionSection, MiniTitle, Image, BlockQuote, Tag,
    ListSection, ListItem
)


class MiniTitleInline(admin.TabularInline):
    model = MiniTitle
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class BlockQuoteInline(admin.TabularInline):
    model = BlockQuote
    extra = 1


class RegionSectionInline(admin.StackedInline):
    model = RegionSection
    extra = 1
    show_change_link = True


class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 1


class ListSectionInline(admin.StackedInline):
    model = ListSection
    extra = 1
    show_change_link = True


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("title",  "created_at", "created_by")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    inlines = [TagInline, RegionSectionInline, ListSectionInline]


@admin.register(RegionSection)
class RegionSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "region", "order")
    list_filter = ("region",)
    search_fields = ("title", "description")
    ordering = ("order",)
    inlines = [MiniTitleInline, ImageInline, BlockQuoteInline]


@admin.register(ListSection)
class ListSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "region")
    search_fields = ("title", "description")
    list_filter = ("region",)
    inlines = [ListItemInline]


admin.site.register(MiniTitle)
admin.site.register(Image)
admin.site.register(BlockQuote)
admin.site.register(Tag)
admin.site.register(ListItem)
