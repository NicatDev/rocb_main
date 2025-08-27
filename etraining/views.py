# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils.translation import activate
from .models import Language, Category, TrainingContent, WebinarContent

def language_selection(request):
    """Dil seçimi sayfası (İlk sayfa)"""
    languages = Language.objects.all().order_by('name')
    context = {
        'languages': languages,
        'page_title': 'Choose your language / Выберите свой язык'
    }
    return render(request, 'language_selection.html', context)

def content_type_selection(request, language_code):
    """Read/Watch seçimi sayfası"""
    language = get_object_or_404(Language, code=language_code)
    
    # Dil aktivasyonu
    activate(language_code)
    
    context = {
        'language': language,
        'page_title': 'Choose how you would like to proceed'
    }
    return render(request, 'content_type_selection.html', context)

def read_content_list(request, language_code):
    """Read içerikleri listesi"""
    language = get_object_or_404(Language, code=language_code)
    activate(language_code)
    
    # Kategoriler ve içeriklerini al
    categories = Category.objects.filter(
        is_active=True,
        contents__language=language,
        contents__content_type='read',
        contents__is_active=True
    ).distinct().prefetch_related(
        'contents'
    )
    
    # Her kategori için read içeriklerini filtrele
    for category in categories:
        category.read_contents = category.contents.filter(
            language=language,
            content_type='read',
            is_active=True
        ).order_by('order')
    
    context = {
        'language': language,
        'categories': categories,
        'page_title': f'E-Training: Read in {language.name}'
    }
    return render(request, 'read_content_list.html', context)

def watch_content_list(request, language_code):
    """Watch içerikleri listesi"""
    language = get_object_or_404(Language, code=language_code)
    activate(language_code)
    
    # Webinar içerikleri
    webinars = WebinarContent.objects.filter(
        language=language,
        is_active=True
    ).order_by('order')
    
    # Diğer kategoriler
    categories = Category.objects.filter(
        is_active=True,
        contents__language=language,
        contents__content_type='watch',
        contents__is_active=True
    ).distinct().prefetch_related('contents')
    
    # Her kategori için watch içeriklerini filtrele
    for category in categories:
        category.watch_contents = category.contents.filter(
            language=language,
            content_type='watch',
            is_active=True
        ).order_by('order')
    
    context = {
        'language': language,
        'webinars': webinars,
        'categories': categories,
        'page_title': f'E-Training: Watch in {language.name}'
    }
    return render(request, 'watch_content_list.html', context)

def read_content_detail(request, language_code, slug):
    """PDF içerik detayı ve görüntüleme"""
    language = get_object_or_404(Language, code=language_code)
    activate(language_code)
    
    content = get_object_or_404(
        TrainingContent,
        slug=slug,
        language=language,
        content_type='read',
        is_active=True
    )
    
    if not content.pdf_file:
        raise Http404("PDF file not found")
    
    context = {
        'language': language,
        'content': content,
        'page_title': content.title
    }
    return render(request, 'read_content_detail.html', context)

def watch_content_detail(request, language_code, slug):
    """Video içerik detayı"""
    language = get_object_or_404(Language, code=language_code)
    activate(language_code)
    
    content = get_object_or_404(
        TrainingContent,
        slug=slug,
        language=language,
        content_type='watch',
        is_active=True
    )
    
    if not content.video_url and not content.video_embed_code:
        raise Http404("Video content not found")
    
    context = {
        'language': language,
        'content': content,
        'page_title': content.title
    }
    return render(request, 'watch_content_detail.html', context)

def webinar_detail(request, language_code, webinar_id):
    """Webinar detay sayfası"""
    language = get_object_or_404(Language, code=language_code)
    activate(language_code)
    
    webinar = get_object_or_404(
        WebinarContent,
        id=webinar_id,
        language=language,
        is_active=True
    )
    
    context = {
        'language': language,
        'webinar': webinar,
        'page_title': webinar.title
    }
    return render(request, 'webinar_detail.html', context)

# Class-based views alternatifi
class ReadContentListView(ListView):
    """Read içerikleri için class-based view"""
    model = TrainingContent
    template_name = 'training/read_content_list.html'
    context_object_name = 'contents'
    
    def get_queryset(self):
        language_code = self.kwargs['language_code']
        language = get_object_or_404(Language, code=language_code)
        
        return TrainingContent.objects.filter(
            language=language,
            content_type='read',
            is_active=True
        ).select_related('category', 'language').order_by('category__order', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = self.kwargs['language_code']
        context['language'] = get_object_or_404(Language, code=language_code)
        return context

# API endpoints (opsiyonel)
from django.http import JsonResponse

def api_content_by_language(request, language_code, content_type):
    """API: Dile göre içerikleri JSON olarak döndür"""
    language = get_object_or_404(Language, code=language_code)
    
    contents = TrainingContent.objects.filter(
        language=language,
        content_type=content_type,
        is_active=True
    ).select_related('category').values(
        'id', 'title', 'slug', 'description',
        'category__name', 'order', 'thumbnail'
    ).order_by('category__order', 'order')
    
    return JsonResponse({
        'language': language_code,
        'content_type': content_type,
        'contents': list(contents)
    })