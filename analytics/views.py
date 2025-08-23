from django.shortcuts import render
from .models import Analytics


def analytics_page(request, slug=None):
    query = Analytics.objects.all()
    analytics = query[0] if len(query) else {}

    return render(request, "analytics.html", {
        "analytics": analytics,
    })
