import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .openai_translate import OpenAITranslateError, translate_html


@csrf_protect
@require_POST
def translate_html_api(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Invalid JSON body.'}, status=400)

    html = payload.get('html', '')
    source_lang = payload.get('source_language', 'en')
    target_lang = payload.get('target_language', 'ru')

    if not isinstance(html, str) or not html.strip():
        return JsonResponse({'detail': 'HTML content is required.'}, status=400)

    try:
        translated = translate_html(html, source_lang, target_lang)
    except OpenAITranslateError as exc:
        return JsonResponse({'detail': str(exc)}, status=502)

    return JsonResponse({'html': translated})
