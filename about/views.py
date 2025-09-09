from django.shortcuts import render, get_object_or_404
from .models import About, ContactPoint
from django.http import JsonResponse, FileResponse, Http404


def about_page(request, slug=None):
    tabs = list(About.objects.all())
    if not tabs:
        return render(request, "about.html", {
            "tabs": [],
            "selected_tab": None,
            "about": None
        })

    if slug:
        selected_tab = get_object_or_404(About, slug=slug)
    else:
        selected_tab = tabs[0]
    current_index = tabs.index(selected_tab)
    prev_tab = tabs[current_index - 1] if current_index > 0 else None
    next_tab = tabs[current_index + 1] if current_index < len(tabs) - 1 else None

    sections = selected_tab.sections.prefetch_related(
        'mini_titles',
        'images'
    ).order_by('order') 

    tags = selected_tab.tags.all()
    contact_points = ContactPoint.objects.all()

    return render(request, "about.html", {
        "tabs": tabs,
        "selected_tab": selected_tab,
        "about": selected_tab,
        "sections": sections,
        "tags": tags,
        "prev_tab": prev_tab,
        "next_tab": next_tab,
        "contact_points": contact_points,
    })

def about_list(request):
    items = About.objects.all().values('id', 'title', 'slug')
    return JsonResponse(list(items), safe=False)

def contact_point_view(request):
    cp = get_object_or_404(ContactPoint)
    if not cp.file:
        raise Http404("File not found")
    return FileResponse(cp.file.open('rb'), as_attachment=False, filename=cp.file.name)
