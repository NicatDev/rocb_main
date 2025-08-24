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


def news_page(request):
    searchParam = request.GET.get("s")
    tagParam = request.GET.get('t')
    page_number = request.GET.get("page", 1)

    news = News.objects.all()
    tags = News.objects.values_list("tag", flat=True).distinct()

    if searchParam:
        news = news.filter(
            Q(title__icontains=searchParam) | Q(tag__icontains=searchParam)
        )

    if tagParam: 
        news = news.filter(tag=tagParam)

    paginator = Paginator(news, 1)
    page_obj = paginator.get_page(page_number)

    others = News.objects.exclude(id__in=[n.id for n in page_obj]).order_by('-id')[:3]

    context = {
        "items": news,
        "tags":tags,
        "page_obj": page_obj,
        "paginator": paginator,
        "others":others
    }

    return render(request, 'news.html', context)

def news_detail(request, slug):
    item = News.objects.get(slug=slug)
    items = News.objects.exclude(slug=slug)[0:3]

    prev_item = News.objects.filter(id__lt=item.id).order_by('-id').first()
    next_item = News.objects.filter(id__gt=item.id).order_by('id').first()

    others = News.objects.exclude(slug=slug).order_by('-id')[0:4]

    context = {
        "item": item,
        "items":items,
        "prev_item":prev_item,
        "next_item":next_item,
        "others":others
    }
    return render(request, 'newsDetail.html', context)


def events_page(request):
    searchParam = request.GET.get("s")
    tagParam = request.GET.get('t')
    page_number = request.GET.get("page", 1)

    events = Event.objects.all()
    tags = Event.objects.values_list("tag", flat=True).distinct()

    if searchParam:
        events = events.filter(
            Q(title__icontains=searchParam) | Q(tag__icontains=searchParam)
        )

    if tagParam: 
        events = events.filter(tag=tagParam)

    paginator = Paginator(events, 1)
    page_obj = paginator.get_page(page_number)

    others = Event.objects.exclude(id__in=[n.id for n in page_obj]).order_by('-id')[:3]

    context = {
        "items": events,
        "tags":tags,
        "page_obj": page_obj,
        "paginator": paginator,
        "others":others
    }

    return render(request, 'events.html', context)

def events_detail(request, slug):
    item = Event.objects.get(slug=slug)
    items = Event.objects.exclude(slug=slug)[0:3]

    prev_item = Event.objects.filter(id__lt=item.id).order_by('-id').first()
    next_item = Event.objects.filter(id__gt=item.id).order_by('id').first()

    others = Event.objects.exclude(slug=slug).order_by('-id')[0:4]

    context = {
        "item": item,
        "items":items,
        "prev_item":prev_item,
        "next_item":next_item,
        "others":others
    }
    return render(request, 'eventsDetail.html', context)