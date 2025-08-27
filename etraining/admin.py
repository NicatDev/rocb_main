# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Language, Category, TrainingContent, WebinarContent

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(TrainingContent)
class TrainingContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'category', 'content_type', 'file_status', 'is_active', 'order', 'created_at')
    list_filter = ('content_type', 'language', 'category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'category', 'language', 'content_type', 'description', 'image')
        }),
        ('Read İçeriği (PDF)', {
            'fields': ('pdf_file',),
            'classes': ('collapse',),
        }),
        ('Watch İçeriği (Video)', {
            'fields': ('video_url',),
            'classes': ('collapse',),
        }),
        ('Ayarlar', {
            'fields': ('order', 'is_active'),
        }),
    )
    
    def file_status(self, obj):
        if obj.content_type == 'read':
            if obj.pdf_file:
                return format_html(
                    '<span style="color: green;">✓</span> <a href="{}" target="_blank">PDF</a>',
                    obj.pdf_file.url
                )
            else:
                return format_html('<span style="color: red;">✗ No PDF</span>')
        elif obj.content_type == 'watch':
            if obj.video_url:
                if obj.video_url:
                    return format_html(
                        '<span style="color: green;">✓</span> <a href="{}" target="_blank">Video</a>',
                        obj.video_url
                    )
                else:
                    return format_html('<span style="color: green;">✓ Embed Code</span>')
            else:
                return format_html('<span style="color: red;">✗ No Video</span>')
        return '-'
    file_status.short_description = 'File Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('language', 'category')

@admin.register(WebinarContent)
class WebinarContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'webinar_link', 'is_active', 'created_at')
    list_filter = ('language', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ('title',)
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'description', 'language')
        }),
        ('Video Bilgileri', {
            'fields': ('webinar_url',),
        }),
        ('Ayarlar', {
            'fields': ('is_active',),
        }),
    )
    
    def webinar_link(self, obj):
        if obj.webinar_url:
            return format_html('<a href="{}" target="_blank">Open Webinar</a>', obj.webinar_url)
        return '-'
    webinar_link.short_description = 'Webinar Link'

admin.site.site_header = "E-Training Admin"
admin.site.site_title = "E-Training"
admin.site.index_title = "E-Training Administration"

class TrainingContentInline(admin.TabularInline):
    model = TrainingContent
    extra = 0
    fields = ('title', 'content_type', 'order', 'is_active')
    readonly_fields = ('created_at',)

class CategoryWithContentsAdmin(CategoryAdmin):
    inlines = [TrainingContentInline]

class LanguageWithContentsAdmin(LanguageAdmin):
    inlines = [TrainingContentInline]

admin.site.unregister(Category)
admin.site.unregister(Language)
admin.site.register(Category, CategoryWithContentsAdmin)
admin.site.register(Language, LanguageWithContentsAdmin)