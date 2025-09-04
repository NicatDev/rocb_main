from modeltranslation.translator import register, TranslationOptions
from .models import (
    MetaInfo, BaseMixin, News, NewsSection, Event, EventSection,
    MeetingDocuments, DocumentExperts, DocumentFiles,
    MeetingRegistrations, Faq
)

@register(MetaInfo)
class MetaInfoTranslationOptions(TranslationOptions):
    fields = ('meta_title', 'meta_description', 'meta_keyword', 'image_alt')

@register(BaseMixin)
class BaseMixinTranslationOptions(TranslationOptions):
    fields = ('meta_title', 'meta_description', 'meta_keyword', 'image_alt')

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'tag')

@register(NewsSection)
class NewsSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'tag')

@register(EventSection)
class EventSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(MeetingDocuments)
class MeetingDocumentsTranslationOptions(TranslationOptions):
    fields = ('title', 'location')

@register(DocumentExperts)
class DocumentExpertsTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(DocumentFiles)
class DocumentFilesTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(MeetingRegistrations)
class MeetingRegistrationsTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')