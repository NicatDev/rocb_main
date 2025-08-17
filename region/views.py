from django.shortcuts import render, get_object_or_404
from .models import Region


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
        'list_items').all()

    return render(request, "region.html", {
        "regiontabs": regiontabs,
        "selected_tab": selected_tab,
        "region": selected_tab,
        "sections": sections,
        "tags": tags,
        "list_sections": list_sections,
        "prev_tab": prev_tab,
        "next_tab": next_tab
    })
