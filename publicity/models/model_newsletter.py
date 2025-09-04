from django.db import models

class Newsletter(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description", null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return self.title


class NewsletterItems(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    order = models.PositiveIntegerField(null=True, blank=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name="items")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        items = NewsletterItems.objects.filter(newsletter=self.newsletter).order_by("order", "id")

        for idx, item in enumerate(items, start=1):
            if item.order != idx:
                item.order = idx
                super(NewsletterItems, item).save(update_fields=["order"])
