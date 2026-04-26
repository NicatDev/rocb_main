from django import template
from django.http import QueryDict

register = template.Library()


@register.filter
def news_seo_robots(language_code) -> str:
    """index only for English news URLs; other locales noindex."""
    if (language_code or '').lower() == 'en':
        return 'index, follow'
    return 'noindex, follow'


@register.filter
def removetag(value, param_name):
    query_dict = QueryDict(value, mutable=True)
    query_dict.pop(param_name, None)
    return query_dict.urlencode()