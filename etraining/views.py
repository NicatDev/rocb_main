from django.shortcuts import render
from .models import  ECategory
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

@login_required
def etraining(request, is_video):
    lang = get_language()
    categories = ECategory.objects.filter(lang_code=lang)
    context = {
        'categories':categories,
        'lang':lang,
        'is_video':is_video
    }
    return render(request, "etrainings.html", context)