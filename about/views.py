from django.shortcuts import render, get_object_or_404
from .models import About
from region.models import Region


def about_page(request, slug=None):
    tabs = list(About.objects.order_by('created_at'))
    regiontabs = list(Region.objects.order_by('created_at'))

    if not regiontabs:
        return render(request, "about.html", {
            "regiontabs": [],
            "selected_region": None,
        })

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
    next_tab = tabs[current_index +
                    1] if current_index < len(tabs) - 1 else None

    sections = selected_tab.sections.prefetch_related(
        'mini_titles', 'images', 'block_quotes'
    ).all()
    tags = selected_tab.tags.all()

    return render(request, "about.html", {
        "tabs": tabs,
        "selected_tab": selected_tab,
        "about": selected_tab,
        "sections": sections,
        "tags": tags,
        "prev_tab": prev_tab,
        "next_tab": next_tab,
        "regiontabs": regiontabs,
    })
