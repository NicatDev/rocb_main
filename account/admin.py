from django.contrib import admin
from .models import Profile
from modeltranslation.admin import TabbedTranslationAdmin

@admin.register(Profile)
class ProfileAdmin(TabbedTranslationAdmin):
    list_display = ('user', 'organization', 'position')