from django.contrib import admin
from publicity.model_newsletter import Newsletter, NewsletterItems


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





