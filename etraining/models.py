from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Language(models.Model):
    name = models.CharField(max_length=50, help_text="Dil adı")
    code = models.CharField(max_length=10, unique=True, help_text="Dil kodu (örneğin: en, fr, es)", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class TrainingContent(models.Model):    
    CONTENT_TYPE_CHOICES = [
        ('read', _('Read')),
        ('watch', _('Watch')),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='contents')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # PDF için
    pdf_file = models.FileField(
        upload_to='training/pdfs/%Y/%m/', 
        blank=True, 
        null=True,
        help_text="Read tipindeki içerikler için PDF dosyası"
    )
    
    # Video için
    video_url = models.URLField(
        blank=True, 
        help_text="Watch tipindeki içerikler için video URL'si"
    )
    # image
    image = models.ImageField(
        upload_to='training/images/%Y/%m/', 
        blank=True,
        help_text="İçerik önizleme resmi"
    )
    
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Training Content")
        verbose_name_plural = _("Training Contents")
        ordering = ['order', 'title']
        unique_together = ['slug', 'language']
    
    def __str__(self):
        return f"{self.title} ({self.language.name}) - {self.get_content_type_display()}"
    
    def get_absolute_url(self):
        if self.content_type == 'read':
            return reverse('training:content_read', kwargs={
                'language': self.language.name,
                'slug': self.slug
            })
        else:
            return reverse('training:content_watch', kwargs={
                'language': self.language.name, 
                'slug': self.slug
            })
    
    def get_file_url(self):
        if self.content_type == 'read' and self.pdf_file:
            return self.pdf_file.url
        elif self.content_type == 'watch' and self.video_url:
            return self.video_url
        return None

class WebinarContent(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    
    webinar_url = models.URLField(help_text="Webinar linki")    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Webinar Content")
        verbose_name_plural = _("Webinar Contents")
        ordering = ('title',)
    
    def __str__(self):
        return f"{self.title} - ({self.language.name})"