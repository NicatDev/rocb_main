from django.contrib import admin
from .models import ETrainingDocs, ETrainingVideo, ECategory
from modeltranslation.admin import TabbedTranslationAdmin

@admin.register(ECategory)
class ECategoryAdmin(TabbedTranslationAdmin):
    list_display = ('title',)

@admin.register(ETrainingVideo)
class ETrainingVideoAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'category')

@admin.register(ETrainingDocs)
class ETrainingDocsAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'category')