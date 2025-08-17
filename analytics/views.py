from django.shortcuts import render
from .models import Analytics


def analytics_page(request, slug=None):
    analytics = Analytics.objects.all()[0]

    return render(request, "analytics.html", {
        "analytics": analytics,
    })
