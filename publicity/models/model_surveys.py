from django.utils.text import slugify
from django.db import models


class Survey(models.Model):  # Fixed typo: çodel -> Model
    title = models.CharField(max_length=200, verbose_name="Title")
    file = models.FileField(upload_to='surveys/', verbose_name="Survey File")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return self.title

    