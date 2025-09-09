from django.contrib import admin
from .models import About, AboutSection, MiniTitle, Image, Tag
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

class AboutSectionInline(TranslationTabularInline):
    model = AboutSection
    extra = 1


@admin.register(About)
class AboutAdmin(TabbedTranslationAdmin):
    list_display = ("title",)
    inlines = [AboutSectionInline]


@admin.register(AboutSection)
class AboutSectionAdmin(TabbedTranslationAdmin):
    list_display = ("title", "about", "order")
    list_editable = ("order",)


@admin.register(MiniTitle)
class MiniTitleAdmin(TabbedTranslationAdmin):
    list_display = ("title", "aboutsection")


@admin.register(Image)
class ImageAdmin(TabbedTranslationAdmin):
    list_display = ("alttag", "aboutsection")


@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin):
    list_display = ("title", "about")

from .models import ContactPoint

@admin.register(ContactPoint)
class ContactPointAdmin(TabbedTranslationAdmin):
    def has_add_permission(self, request):
        if ContactPoint.objects.exists():
            return False
        return True