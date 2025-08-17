from django.utils.text import slugify
from django.db import models


class Analytics(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, editable=False, blank=True, null=True)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to='analytics_images/', verbose_name="Image", blank=True, null=True)

    class Meta:
        verbose_name = "Analytic"
        verbose_name_plural = "Analytics"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class AnalyticsSection(models.Model):
    analytics = models.ForeignKey(
        Analytics, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200, verbose_name="Section Title")
    description = models.TextField(verbose_name="Section Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    class Meta:
        verbose_name = "Analytics Section"
        verbose_name_plural = "Analytics Sections"
        ordering = ['order']

    def __str__(self):
        return f"{self.analytics.title} - {self.title}"



class Image(models.Model):
    analyticsSection = models.ForeignKey(
        AnalyticsSection, on_delete=models.CASCADE, related_name='images')
    alttag = models.CharField(
        max_length=200, verbose_name="Alt Tag", blank=True, null=True)
    image = models.ImageField(upload_to='analytics_images/', verbose_name="Image")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image for {self.analyticsSection.title}"


