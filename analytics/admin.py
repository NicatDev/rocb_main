from django.contrib import admin
from .models import Analytics, AnalyticsSection, Image


class AnalyticsSectionInline(admin.TabularInline):
    model = AnalyticsSection
    extra = 1


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [AnalyticsSectionInline]


@admin.register(AnalyticsSection)
class AnalyticsSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "analytics", "order")
    list_editable = ("order",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("alttag", "analyticsSection")


