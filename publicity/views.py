from django.shortcuts import render
from .model_newsletter import Newsletter


def newsletter_page(request, slug=None):
    newsletters = Newsletter.objects.all()

    return render(request, "newsletter.html", {
        "newsletters": newsletters,
    })
