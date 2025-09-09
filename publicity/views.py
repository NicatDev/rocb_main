from .models.model_surveys import Survey
import os
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, get_object_or_404
from .models.model_cct_center import CCTCenter, CCT_Center_Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models.model_newsletter import Newsletter
from .models.model_gallery import Gallery
from .models.model_outreach_materials import Outreach, OutreachEmbed
from django.contrib.auth.decorators import login_required

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
        "embeds": embeds
    })


def gallery_page(request, slug=None):
    gallery_items = Gallery.objects.all().order_by('order')

    paginator = Paginator(gallery_items, 6)
    page = request.GET.get('page', 1)

    try:
        gallery = paginator.page(page)
    except PageNotAnInteger:
        gallery = paginator.page(1)
    except EmptyPage:
        gallery = paginator.page(paginator.num_pages)

    return render(request, "gallery.html", {
        "gallery": gallery,
        "paginator": paginator,
    })


def cct_center_page(request):
    cct_centers = CCTCenter.objects.first()
    images = CCT_Center_Image.objects.filter(cctcenter=cct_centers)

    return render(request, "cct_center.html", {
        "cct_centers": cct_centers,
        "images": images,
    })


def utilize_our_premises_page(request):
    return render(request, "utilize_our_premises.html", {})

@login_required
def survey_page(request):
    surveys = Survey.objects.all()
    context = {
        'surveys': surveys
    }
    return render(request, "surveys.html", context)

@login_required
def survey_pdf_view(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if not survey.file:
        raise Http404("Survey file not found")

    file_path = survey.file.path
    if not os.path.exists(file_path):
        raise Http404("Survey file does not exist")

    try:
        return FileResponse(
            open(file_path, 'rb'),
            content_type='application/pdf',
            filename=f"{survey.title}.pdf"
        )
    except IOError:
        raise Http404("Error opening survey file")
