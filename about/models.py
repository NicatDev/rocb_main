from django.utils.text import slugify
from django.db import models


class About(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    map = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, editable=False, blank=True, null=True)
    description = models.TextField(
        verbose_name="Description", blank=True, null=True)
    image = models.ImageField(
        upload_to='about_images/', verbose_name="Image", blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    position = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "Abouts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class AboutSection(models.Model):
    about = models.ForeignKey(
        About, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(
        max_length=200, verbose_name="Section Title", blank=True, null=True)
    description = models.TextField(
        verbose_name="Section Description", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"
        ordering = ['order']

    def __str__(self):
        return f"{self.about.title} - {self.title}"


class MiniTitle(models.Model):
    title = models.CharField(max_length=200, verbose_name="Mini Title")
    aboutsection = models.ForeignKey(
        AboutSection, on_delete=models.CASCADE, related_name='mini_titles')

    class Meta:
        verbose_name = "Mini Title"
        verbose_name_plural = "Mini Titles"

    def __str__(self):
        return self.title


class Image(models.Model):
    aboutsection = models.ForeignKey(
        AboutSection, on_delete=models.CASCADE, related_name='images')
    alttag = models.CharField(
        max_length=200, verbose_name="Alt Tag", blank=True, null=True)
    image = models.ImageField(upload_to='about_images/', verbose_name="Image")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image for {self.aboutsection.title}"


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag Name")
    about = models.ForeignKey(
        About, on_delete=models.CASCADE, related_name='tags', blank=True, null=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.title

from django.core.exceptions import ValidationError

class ContactPoint(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='contact_point/')

    def save(self, *args, **kwargs):
        if not self.pk and ContactPoint.objects.exists():
            raise ValidationError("Sadece bir ContactPoint kaydı eklenebilir.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Contact Point"
