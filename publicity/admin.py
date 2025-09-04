from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from publicity.models.model_newsletter import Newsletter, NewsletterItems
from publicity.models.model_outreach_materials import Outreach, OutreachEmbed
from publicity.models.model_gallery import Gallery
from publicity.models.model_cct_center import CCTCenter, CCT_Center_Image
from publicity.models.model_surveys import Survey


class NewsletterItemsInline(TranslationTabularInline):
    model = NewsletterItems
    extra = 1


@admin.register(Newsletter)
class NewsletterAdmin(TabbedTranslationAdmin):
    list_display = ("title",)
    inlines = [NewsletterItemsInline]


@admin.register(NewsletterItems)
class NewsletterItemsAdmin(TabbedTranslationAdmin): 
    list_display = ("title", "newsletter", "order")
    list_editable = ("order",)


@admin.register(Outreach)
class OutreachAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'high')


@admin.register(OutreachEmbed)
class OutreachEmbedAdmin(TabbedTranslationAdmin):
    list_display = ('title',)


@admin.register(CCTCenter)
class CCTCenterAdmin(TabbedTranslationAdmin):
    list_display = ('title',)


@admin.register(CCT_Center_Image)
class CCT_Center_ImageAdmin(TabbedTranslationAdmin):
    list_display = ('alttag', 'cctcenter')


@admin.register(Survey)
class SurveyAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'start_date', 'end_date')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')