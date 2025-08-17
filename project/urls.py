# from oneapp.sitemap import BlogSiteMap,ServiceSiteMap,StaticSitemap
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
# from marketapp.sitemap import BlogSiteMap,ServiceSitemap, StaticSitemap
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns


# sitemaps = {
#     'blog_sitepap':BlogSiteMap,
#     'service_sitemap': ServiceSiteMap,
#     'static_sitemap': StaticSitemap,
# }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('robots.txt/', TemplateView.as_view(template_name='robots.txt',
         content_type="text/plain")),
]

urlpatterns += i18n_patterns(
    re_path(r'^rosetta/', include('rosetta.urls')),
    path('', include("oneapp.urls")),
    path('', include("contact.urls")),
    path('', include("about.urls")),
    path('', include("region.urls")),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
