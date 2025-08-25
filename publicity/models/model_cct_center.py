from django.utils.text import slugify
from django.db import models


class CCTCenter(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to='cct_center_image/', verbose_name="Image", blank=True, null=True)

    class Meta:
        verbose_name = "CCT Center"
        verbose_name_plural = "CCT Centers"

    def __str__(self):
        return self.title


class CCT_Center_Image(models.Model):
    cctcenter = models.ForeignKey(
        CCTCenter, on_delete=models.CASCADE, related_name='cct_center_images')
    alttag = models.CharField(
        max_length=200, verbose_name="Alt Tag", blank=True, null=True)
    image = models.ImageField(
        upload_to='cct_center_images/', verbose_name="Image")

    class Meta:
        verbose_name = "CCT Center Image"
        verbose_name_plural = "CCT Center Images"

    def __str__(self):
        return f"Image for {self.cctcenter.title}"
