from modeltranslation.translator import TranslationOptions,register, translator
from oneapp.models import News, NewsSection, Event, EventSection

# ------------------- News ------------------- #

class NewsTranslationOption(TranslationOptions):
    fields = ('title','description','meta_title','meta_description')

class NewsSectionTranslationOption(TranslationOptions):
    fields = ('title','description')

translator.register(News, NewsTranslationOption)
translator.register(NewsSection, NewsSectionTranslationOption)

# ------------------- News ------------------- #

# ------------------- Event ------------------- #

class EventTranslationOption(TranslationOptions):
    fields = ('title','description','meta_title','meta_description')

class EventSectionTranslationOption(TranslationOptions):
    fields = ('title','description')

translator.register(Event, EventTranslationOption)
translator.register(EventSection, EventSectionTranslationOption)

# ------------------- Event ------------------- #