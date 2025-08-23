from django.db import models

class Outreach(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description", null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    high = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Outreach material"
        verbose_name_plural = "Outreach materials"

    def __str__(self):
        return self.title

class OutreachEmbed(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    embed = models.CharField(max_length=3000, null=True,blank=True)

    class Meta:
        verbose_name = "OutreachEmbed"
        verbose_name_plural = "OutreachEmbeds"

    def __str__(self):
        return self.title

