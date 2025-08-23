from django.contrib import admin
from publicity.models.model_newsletter import Newsletter, NewsletterItems
from publicity.models.model_outreach_materials import Outreach, OutreachEmbed

class NewsletterItemsInline(admin.TabularInline):
    model = NewsletterItems
    extra = 1


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [NewsletterItemsInline]


@admin.register(NewsletterItems)
class NewsletterItemsAdmin(admin.ModelAdmin):
    list_display = ("title", "newsletter", "order")
    list_editable = ("order",)

admin.site.register(Outreach)
admin.site.register(OutreachEmbed)



