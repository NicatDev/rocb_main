from django.utils.text import slugify
from django.db import models


class Survey(models.Model):  # Fixed typo: çodel -> Model
    title = models.CharField(max_length=200, verbose_name="Title")
    file = models.FileField(upload_to='surveys/', verbose_name="Survey File")
    start_date = models.DateField(
        verbose_name="Start Date", help_text="Event/Survey start date")
    end_date = models.DateField(
        verbose_name="End Date", help_text="Event/Survey end date")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def get_date_range_display(self):
        """Returns formatted date range string"""
        if self.start_date == self.end_date:
            return self.start_date.strftime("%d %B %Y")

        # Same month and year
        if self.start_date.month == self.end_date.month and self.start_date.year == self.end_date.year:
            return f"{self.start_date.day}-{self.end_date.day} {self.start_date.strftime('%B %Y')}"

        # Same year, different months
        elif self.start_date.year == self.end_date.year:
            return f"{self.start_date.strftime('%d %B')}-{self.end_date.strftime('%d %B %Y')}"

        # Different years
        else:
            return f"{self.start_date.strftime('%d %B %Y')}-{self.end_date.strftime('%d %B %Y')}"
