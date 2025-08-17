from django.db import models
from oneapp.utils import get_url_names, slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
URL_CHOICES = [
    ('home', 'home'),
    ('about', 'about'),
    ('blogs', 'blogs'),
    ('services', 'services'),
    ('portfolios', 'portfolios'),
    ('contact', 'contact'),
]


class MetaInfo(models.Model):
    page_name = models.CharField(
        max_length=300, choices=URL_CHOICES, unique=True)
    meta_title = models.CharField(
        max_length=10, null=True, blank=True, verbose_name='title for seo')
    meta_description = models.CharField(
        max_length=300, null=True, blank=True, verbose_name='Meta Description')
    meta_keyword = models.CharField(
        max_length=300, null=True, blank=True, verbose_name='keywords for seo')
    image_alt = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.page_name

    def delete(self, *args, **kwargs):
        raise ValidationError("Meta məlumatları silinə bilməz!")


class BaseMixin(models.Model):
    slug = models.SlugField(unique=True, editable=False, blank=True, null=True)
    created_at = models.DateField(auto_now=True, blank=True, null=True,)
    meta_title = models.CharField(
        max_length=60, null=True, blank=True, verbose_name='title for seo')
    meta_description = models.CharField(
        max_length=160, null=True, blank=True, verbose_name='description for seo')
    meta_keyword = models.CharField(
        max_length=160, null=True, blank=True, verbose_name='keyword for seo')
    image_alt = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        abstract = True


class News(BaseMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    in_home = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    tag = models.CharField(max_length=200, null=True,blank=True)
    
    def __str__(self):
        return f'-{self.title}'

    def get_absolute_url(self):
        return reverse('news-single', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            self.slug = new_slug
            if News.objects.filter(slug=new_slug).exists():
                count = 0
                while News.objects.filter(slug=new_slug).exists():
                    new_slug = f"{slugify(self.title)}-{count}"
                    count += 1
        super(News, self).save(*args, **kwargs)


class NewsSection(models.Model):
    parent = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='news_sections')
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'-{self.title}'


class Event(BaseMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    in_home = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    tag = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return f'-{self.title}'

    def get_absolute_url(self):
        return reverse('event-single', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            self.slug = new_slug
            if Event.objects.filter(slug=new_slug).exists():
                count = 0
                while Event.objects.filter(slug=new_slug).exists():
                    new_slug = f"{slugify(self.title)}-{count}"
                    count += 1
        super(Event, self).save(*args, **kwargs)


class EventSection(models.Model):
    parent = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_sections')
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'-{self.title}'
