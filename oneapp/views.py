from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.utils import translation
from django.urls.exceptions import Resolver404
from urllib.parse import urlparse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
import random

from about.models import About
from region.models import Region

from .models import News, Event


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response


def home(request):
    events = Event.objects.filter(in_home=True)[0:8]
    news = News.objects.filter(in_home=True)[0:8]
    tabs = About.objects.order_by('created_at')
    regiontabs = Region.objects.order_by('created_at')

    context = {
        "events": events,
        "news": news,
        "tabs": tabs,
        "regiontabs": regiontabs,
    }

    return render(request, 'index.html', context)
