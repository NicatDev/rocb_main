from django.utils.text import slugify
from django.db import models


class Region(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, editable=False, blank=True, null=True)
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to='region_images/', verbose_name="Image", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")
    created_by = models.CharField(
        max_length=100, verbose_name="Created By", blank=True, null=True)

    autorized_image = models.ImageField(
        upload_to='region_images/', verbose_name="Authorized Image", blank=True, null=True)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class RegionSection(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200, verbose_name="Section Title")
    description = models.TextField(verbose_name="Section Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    class Meta:
        verbose_name = "Region Section"
        verbose_name_plural = "Region Sections"
        ordering = ['order']

    def __str__(self):
        return f"{self.region.title} - {self.title}"


class MiniTitle(models.Model):
    title = models.CharField(max_length=200, verbose_name="Mini Title")
    regionsection = models.ForeignKey(
        RegionSection, on_delete=models.CASCADE, related_name='mini_titles')

    class Meta:
        verbose_name = "Mini Title"
        verbose_name_plural = "Mini Titles"

    def __str__(self):
        return self.title


class Image(models.Model):
    regionsection = models.ForeignKey(
        RegionSection, on_delete=models.CASCADE, related_name='images')
    alttag = models.CharField(
        max_length=200, verbose_name="Alt Tag", blank=True, null=True)
    image = models.ImageField(upload_to='region_images/', verbose_name="Image")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image for {self.regionsection.title}"


class BlockQuote(models.Model):
    regionsection = models.ForeignKey(
        RegionSection, on_delete=models.CASCADE, related_name='block_quotes')
    fullname = models.CharField(max_length=200, verbose_name="Full Name")
    content = models.TextField(verbose_name="Content")

    class Meta:
        verbose_name = "Block Quote"
        verbose_name_plural = "Block Quotes"

    def __str__(self):
        return f"{self.fullname} - {self.content[:50]}..."


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag Name")
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='tags', blank=True, null=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.title


class ListSection(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='list_sections')
    title = models.CharField(max_length=200, verbose_name="List Section Title")
    description = models.TextField(verbose_name="List Section Description")

    class Meta:
        verbose_name = "List Section"
        verbose_name_plural = "List Sections"
        ordering = ['title']

    def __str__(self):
        return self.title
    

class ListItem(models.Model):
    list_section = models.ForeignKey(
        ListSection, on_delete=models.CASCADE, related_name='list_items')
    title = models.CharField(max_length=200, verbose_name="List Item Title")
    description = models.TextField(verbose_name="List Item Description")

    class Meta:
        verbose_name = "List Item"
        verbose_name_plural = "List Items"
        ordering = ['title']

    def __str__(self):
        return self.title
    
    