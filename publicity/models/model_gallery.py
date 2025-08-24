from django.db import models


class Gallery(models.Model):
    image = models.ImageField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Gallery item"
        verbose_name_plural = "Gallery items"
        ordering = ['order']

    def __str__(self):
        return f"Gallery Item {self.id}"
