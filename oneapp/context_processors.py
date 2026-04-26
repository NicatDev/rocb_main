from django.conf import settings


def public_site_url(request):
    return {
        'public_site': getattr(settings, 'PUBLIC_SITE_URL', 'https://rocb-europe.org').rstrip('/'),
    }
