from django.contrib import admin
from .models import (
    Registration, Event, EventSection, News, NewsSection,
    MeetingRegistrations, Faq, MeetingDocuments, DocumentExperts, DocumentFiles
)
from modeltranslation.admin import (
    TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline
)

class EventModelInline(TranslationStackedInline):
    model = EventSection
    extra = 0

class NewsModelInline(TranslationStackedInline):
    model = NewsSection
    extra = 0

class DocumentExpertsInline(TranslationTabularInline):
    model = DocumentExperts
    extra = 1

class DocumentFilesInline(TranslationTabularInline):
    model = DocumentFiles
    extra = 1

@admin.register(Event)
class EventAdmin(TabbedTranslationAdmin):
    list_display = ("title",)
    inlines = [EventModelInline]

@admin.register(News)
class NewsAdmin(TabbedTranslationAdmin): 
    list_display = ("title",)
    inlines = [NewsModelInline]

@admin.register(MeetingRegistrations)
class MeetingRegisterAdmin(TabbedTranslationAdmin):
    list_display = ("title", "timezone")

@admin.register(MeetingDocuments)
class MeetingDocumentsAdmin(TabbedTranslationAdmin): 
    list_display = ("title", "date", "location")
    inlines = [DocumentExpertsInline, DocumentFilesInline]

@admin.register(DocumentExperts)
class DocumentExpertsAdmin(TabbedTranslationAdmin): 
    list_display = ("title", "document")

@admin.register(DocumentFiles)
class DocumentFilesAdmin(TabbedTranslationAdmin): 
    list_display = ("title", "file")

@admin.register(Faq)
class FaqAdmin(TabbedTranslationAdmin): 
    list_display = ("question",) 

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_at')
    readonly_fields = ('full_name', 'phone_number', 'email', 'subject', 'created_at',
                       'organization', 'position', 'note')