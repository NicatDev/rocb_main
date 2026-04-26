from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from oneapp.sitemap import HomeSitemap, NewsIndexSitemap, NewsSitemap
from oneapp.views import robots_txt

admin.site.site_header = 'Rocb Europe Admin'
admin.site.site_title = 'Rocb Europe Admin'
admin.site.index_title = 'Rocb Europe Admin'

sitemaps = {
    'home': HomeSitemap,
    'news_index': NewsIndexSitemap,
    'news': NewsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += i18n_patterns(
    re_path(r'^rosetta/', include('rosetta.urls')),
    path('', include("oneapp.urls")),
    path('', include("contact.urls")),
    path('', include("about.urls")),
    path('', include("region.urls")),
    path('', include("account.urls")),
    path('', include("analytics.urls")),
    path('publicity/', include("publicity.urls")),
    path('', include("etraining.urls")),
)

# DEBUG=True: staticfiles app serves /static/ from STATICFILES_DIRS (no urlpattern needed).
# DEBUG=False: run collectstatic, then nginx (or similar) should serve STATIC_ROOT at STATIC_URL.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
