from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods

from oneapp.news_api_client import fetch_main_site_rtc_profiles
from .country_api import serialize_country
from .forms import AdditionalInformationFormSet, CountryOwnerForm
from .models import Region, ListSection, MiniTitle, Image, BlockQuote, ListItem, Tag, Country

REGION_RTC_API_SLUG = 'wco-europe-rtcs'


def region_page(request, slug=None):
    regiontabs = list(Region.objects.order_by('created_at'))

    if not regiontabs:
        return render(request, "region.html", {
            "resgiontabs": [],
            "selected_tab": None,
            "region": None
        })

    if slug:
        selected_tab = get_object_or_404(Region, slug=slug)
    else:
        selected_tab = regiontabs[0]

    current_index = regiontabs.index(selected_tab)
    prev_tab = regiontabs[current_index - 1] if current_index > 0 else None
    next_tab = regiontabs[current_index +
                          1] if current_index < len(regiontabs) - 1 else None

    sections = selected_tab.sections.prefetch_related(
        'mini_titles', 'images', 'block_quotes'
    ).all()
    tags = selected_tab.tags.all()

    list_sections = selected_tab.list_sections.prefetch_related(
        'list_items'
    ).order_by('order')

    countries = (
        Country.objects.filter(region=selected_tab)
        .select_related('owner')
        .prefetch_related('additional_information')
        .order_by('title')
    )

    api_rtc_profiles = []
    if selected_tab.slug == REGION_RTC_API_SLUG:
        api_rtc_profiles = fetch_main_site_rtc_profiles() or []

    return render(request, "region.html", {
        "regiontabs": regiontabs,
        "tabs": regiontabs,
        "selected_tab": selected_tab,
        "region": selected_tab,
        "sections": sections,
        "tags": tags,
        "list_sections": list_sections,
        "prev_tab": prev_tab,
        "next_tab": next_tab,
        'countries': countries,
        'api_rtc_profiles': api_rtc_profiles,
    })


def listsection_detail(request, slug):
    list_section = get_object_or_404(ListSection, slug=slug)
    list_sections_tabs = list(ListSection.objects.order_by('order'))

    list_items = list_section.list_items.order_by('order')
    mini_titles = MiniTitle.objects.filter(
        regionsection__region=list_section.region)
    images = Image.objects.filter(regionsection__region=list_section.region)
    blockquotes = BlockQuote.objects.filter(
        regionsection__region=list_section.region)
    tags = Tag.objects.filter(region=list_section.region)
    files = list_section.files.all() 

    current_index = list_sections_tabs.index(list_section)
    prev_tab = list_sections_tabs[current_index - 1] if current_index > 0 else None
    next_tab = list_sections_tabs[current_index + 1] if current_index < len(list_sections_tabs) - 1 else None

    return render(request, "region_detail.html", {
        "list_section": list_section,
        "list_items": list_items,
        "mini_titles": mini_titles,
        "images": images,
        "blockquotes": blockquotes,
        "tags": tags,
        "files": files, 
        "prev_tab": prev_tab,
        "next_tab": next_tab,
    })


def _get_country_or_404(pk):
    return get_object_or_404(
        Country.objects.select_related('owner').prefetch_related('additional_information'),
        pk=pk,
    )


def _user_owns_country(user, country):
    return user.is_authenticated and country.owner_id and country.owner_id == user.id


@require_GET
def country_detail_json(request, pk):
    country = _get_country_or_404(pk)
    return JsonResponse(serialize_country(country, request.user))


@login_required
@require_http_methods(['GET', 'POST'])
def country_owner_edit(request, pk):
    country = _get_country_or_404(pk)
    if not _user_owns_country(request.user, country):
        return HttpResponseForbidden('You are not the owner of this country.')

    if request.method == 'GET':
        form = CountryOwnerForm(instance=country)
        formset = AdditionalInformationFormSet(instance=country, prefix='info')
        return render(request, 'region/partials/country_edit_form.html', {
            'country': country,
            'form': form,
            'formset': formset,
        })

    form = CountryOwnerForm(request.POST, instance=country)
    formset = AdditionalInformationFormSet(request.POST, instance=country, prefix='info')
    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        country = _get_country_or_404(pk)
        return JsonResponse({
            'success': True,
            'country': serialize_country(country, request.user),
        })
    return JsonResponse({
        'success': False,
        'errors': {
            'form': form.errors,
            'formset': formset.errors,
        },
    }, status=400)
