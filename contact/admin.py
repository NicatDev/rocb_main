from django.contrib import admin
from .models import ContactInfo, Contact
from modeltranslation.admin import TabbedTranslationAdmin

@admin.register(ContactInfo)
class ContactInfoAdmin(TabbedTranslationAdmin):
    list_display = ['location', 'phone_number', 'email', 'fax']
    list_filter = ['location']
    search_fields = ['location', 'phone_number', 'email']
    list_editable = ['phone_number', 'email']

    fieldsets = (
        ('Contact Information', {
            'fields': ('location', 'phone_number', 'fax', 'email')
        }),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject']
    readonly_fields = ['created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['name', 'email', 'phone', 'address', 'subject', 'message']
        return self.readonly_fields

    def created_at(self, obj):
        return getattr(obj, 'created_at', 'N/A')
    created_at.short_description = 'Created At'