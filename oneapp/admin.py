from django.contrib import admin
from .models import Event, EventSection, News, NewsSection
from modeltranslation.admin import TranslationAdmin,TranslationStackedInline

class EventModelInline(TranslationStackedInline):  
    model = EventSection
    extra = 0

    class Media:
        group_fieldsets = True 

        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class EventAdmin(TranslationAdmin):
    list_display = ("title",)
    inlines = [EventModelInline]

    class Media:
        group_fieldsets = True 

        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Event,EventAdmin)


class NewsModelInline(TranslationStackedInline):  
    model = NewsSection
    extra = 0

    class Media:
        group_fieldsets = True 

        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class NewsAdmin(TranslationAdmin):
    list_display = ("title",)
    inlines = [NewsModelInline]

    class Media:
        group_fieldsets = True 

        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(News,NewsAdmin)

