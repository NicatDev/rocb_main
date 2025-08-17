from django.contrib import admin
from .models import About, AboutSection, MiniTitle, Image, BlockQuote, Tag


class AboutSectionInline(admin.TabularInline):
    model = AboutSection
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "created_by")
    inlines = [AboutSectionInline]


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "about", "order")
    list_editable = ("order",)


@admin.register(MiniTitle)
class MiniTitleAdmin(admin.ModelAdmin):
    list_display = ("title", "aboutsection")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("alttag", "aboutsection")


@admin.register(BlockQuote)
class BlockQuoteAdmin(admin.ModelAdmin):
    list_display = ("fullname", "aboutsection")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "about")
