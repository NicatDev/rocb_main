from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation

from .news_api_client import fetch_main_site_news_for_sitemap


class RocbSitemap(Sitemap):
    protocol = 'https'

    def get_domain(self, site=None):
        base = getattr(settings, 'PUBLIC_SITE_URL', '') or 'https://rocbeurope.org'
        host = urlparse(base).netloc
        if host:
            return host
        if site is not None and getattr(site, 'domain', None):
            return site.domain
        return 'rocbeurope.org'


class HomeSitemap(RocbSitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return [code for code, _ in settings.LANGUAGES]

    def location(self, lang_code):
        translation.activate(lang_code)
        return reverse('home')


class NewsIndexSitemap(RocbSitemap):
    """English-only /news listing (SEO index)."""

    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return ['en']

    def location(self, _item):
        translation.activate(settings.LANGUAGE_CODE)
        return reverse('news')


class NewsSitemap(RocbSitemap):
    """English-only news detail URLs (SEO index)."""

    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        rows = fetch_main_site_news_for_sitemap()
        out = []
        for row in rows:
            slug = row.get('slug')
            if not slug:
                continue
            lastmod = row.get('lastmod')
            out.append((slug, lastmod))
        return out

    def lastmod(self, item):
        return item[1]

    def location(self, item):
        slug, _lastmod = item
        translation.activate(settings.LANGUAGE_CODE)
        return reverse('news_detail', kwargs={'slug': slug})
