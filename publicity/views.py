from django.shortcuts import render
from .models.model_newsletter import Newsletter
from .models.model_outreach_materials import Outreach, OutreachEmbed

def newsletter_page(request, slug=None):
    newsletters = Newsletter.objects.all()

    return render(request, "newsletter.html", {
        "newsletters": newsletters,
    })


def outreach_page(request, slug=None):
    materials = Outreach.objects.all()
    embeds = OutreachEmbed.objects.all()
    return render(request, "outreach.html", {
        "materials": materials,
        "embeds":embeds
    })
