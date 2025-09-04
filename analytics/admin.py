from django.contrib import admin
from .models import Analytics, AnalyticsSection, Image
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline


class AnalyticsSectionInline(TranslationTabularInline):
    model = AnalyticsSection
    extra = 1


@admin.register(Analytics)
class AnalyticsAdmin(TabbedTranslationAdmin):
    list_display = ("title",)
    inlines = [AnalyticsSectionInline]


@admin.register(AnalyticsSection)
class AnalyticsSectionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "analytics", "order")
    list_editable = ("order",)


@admin.register(Image)
class ImageAdmin(TabbedTranslationAdmin):
    list_display = ("alttag", "analyticsSection")