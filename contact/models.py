from django.db import models
from django.utils import timezone


class ContactInfo(models.Model):
    location = models.CharField(max_length=255, verbose_name="Location")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    fax = models.CharField(
        max_length=20, verbose_name="Fax", blank=True, null=True)
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Infos"

    def __str__(self):
        return f"{self.location} - {self.phone_number}"


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(
        max_length=255, verbose_name="Address", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Phone")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Created At")

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
