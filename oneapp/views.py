from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.utils import translation
from django.urls.exceptions import Resolver404
from urllib.parse import urlparse
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from about.models import About
from region.models import Region
from django.contrib.auth.decorators import login_required
from .models import Event, MeetingDocuments, MeetingRegistrations, Registration, Faq
from .news_api_client import (
    ApiNewsItem,
    SlugRef,
    build_page_from_api,
    discover_tabs_excluding,
    fetch_main_site_news_batch,
    fetch_main_site_news_detail,
    fetch_main_site_news_page,
    prev_next_slugs,
    search_news_rows,
)
import datetime
import pytz

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
    batch = fetch_main_site_news_batch(8)
    news = [
        ApiNewsItem(row, for_detail=False)
        for row in (batch or {}).get('results', [])
    ]
    faqs = Faq.objects.order_by('order')
    context = {
        "events": events,
        "news": news,
        "faqs":faqs
    }

    return render(request, 'index.html', context)


def news_page(request):
    search_param = request.GET.get("s")
    try:
        page_number = int(request.GET.get("page", 1) or 1)
    except ValueError:
        page_number = 1

    page_size = 8
    data = fetch_main_site_news_page(
        page=page_number, page_size=page_size, search=search_param
    )
    page_obj = build_page_from_api(data, page_number, page_size)
    tabs = discover_tabs_excluding(page_obj, limit=3)

    context = {
        "tags": [],
        "page_obj": page_obj,
        "paginator": page_obj.paginator,
        "tabs": tabs,
    }

    return render(request, 'news.html', context)

def news_detail(request, slug):
    raw = fetch_main_site_news_detail(slug)
    if not raw:
        raise Http404()
    item = ApiNewsItem(raw, for_detail=True)

    prev_slug, next_slug = prev_next_slugs(slug)
    prev_item = SlugRef(prev_slug) if prev_slug else None
    next_item = SlugRef(next_slug) if next_slug else None

    items = []
    more = fetch_main_site_news_page(1, page_size=6)
    if more:
        for row in more.get('results', []):
            if row.get('slug') == slug:
                continue
            items.append(ApiNewsItem(row, for_detail=False))
            if len(items) >= 3:
                break

    tab_objs = []
    tab_batch = fetch_main_site_news_page(1, page_size=8)
    if tab_batch:
        for row in tab_batch.get('results', []):
            if row.get('slug') == slug:
                continue
            tab_objs.append(ApiNewsItem(row, for_detail=False))
            if len(tab_objs) >= 4:
                break

    context = {
        "item": item,
        "items": items,
        "prev_item": prev_item,
        "next_item": next_item,
        "tabs": tab_objs,
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

    paginator = Paginator(events, 3)
    page_obj = paginator.get_page(page_number)

    tabs = Event.objects.exclude(id__in=[n.id for n in page_obj]).order_by('-id')[:3]

    context = {
        "items": events,
        "tags":tags,
        "page_obj": page_obj,
        "paginator": paginator,
        "tabs":tabs
    }

    return render(request, 'events.html', context)

def events_detail(request, slug):
    item = Event.objects.get(slug=slug)
    items = Event.objects.exclude(slug=slug)[0:3]

    prev_item = Event.objects.filter(id__lt=item.id).order_by('-id').first()
    next_item = Event.objects.filter(id__gt=item.id).order_by('id').first()

    tabs = Event.objects.exclude(slug=slug).order_by('-id')[0:4]

    context = {
        "item": item,
        "items":items,
        "prev_item":prev_item,
        "next_item":next_item,
        "tabs":tabs
    }
    return render(request, 'eventsDetail.html', context)

@login_required
def meeting_documents(request):
    items = MeetingDocuments.objects.all()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(items, 5)
    page_obj = paginator.get_page(page_number)

    context = {
        "items": items,
        "page_obj": page_obj,
        "paginator": paginator
    }
    return render(request, 'meetingsDoc.html', context)


def meeting_documents_single(request,slug):
    item = MeetingDocuments.objects.get(slug=slug)

    context = {
        "item": item,
    }
    return render(request, 'meetingsDocDetail.html', context)

def meeting_registrations(request):
    items = MeetingRegistrations.objects.all()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(items, 5)
    page_obj = paginator.get_page(page_number)

    context = {
        "items": items,        
        "page_obj": page_obj,
        "paginator": paginator
    }
    return render(request, 'meetingsReg.html', context)


@csrf_exempt
def register_meeting(request):
    if request.method == "POST":
        data = json.loads(request.body)
        full_name = data.get("full_name")
        phone_number = data.get("phone_number")
        email = data.get("email")
        subject = data.get("subject")
        position = data.get("position")
        organization = data.get("organization")
        note = data.get("note")

        registration = Registration.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            subject=subject,
            position=position,
            organization=organization,
            note=note
        )
        return JsonResponse({"status": "success", "id": registration.id})
    return JsonResponse({"status": "error"}, status=400)




def about_region_list(request):
    about_items = list(About.objects.all().values('id', 'title', 'slug'))
    region_items = list(Region.objects.all().values('id', 'title', 'slug'))

    data = {
        "about": about_items,
        "region": region_items
    }
    return JsonResponse(data, safe=False)

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        news_list = search_news_rows(query)
        event_results = Event.objects.filter(title__icontains=query)

        event_list = [
            {
                'title': e.title,
                'description': e.description,
                'image': e.image,
                'date': e.date,
                'slug': e.slug,
                'type': 'Event'
            }
            for e in event_results
        ]

        combined = news_list + event_list

        # Normalize all dates for sorting
        def sort_key(x):
            dt = x['date']
            if dt is None:
                return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            else:
                dt = dt.astimezone(datetime.timezone.utc)
            return dt

        results = sorted(combined, key=sort_key, reverse=True)

    try:
        page_number = int(request.GET.get('page', 1) or 1)
    except ValueError:
        page_number = 1
    paginator = Paginator(results, 5)
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'search_results.html', context)
