"""Server-side HTML cleanup for rich-text fields (CKEditor / admin)."""

import bleach

try:
    from bleach.css_sanitizer import CSSSanitizer
except ImportError:
    CSSSanitizer = None  # type: ignore[misc, assignment]

_ALLOWED_TAGS = frozenset(
    [
        'p',
        'br',
        'strong',
        'b',
        'em',
        'i',
        'u',
        's',
        'sub',
        'sup',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'ul',
        'ol',
        'li',
        'a',
        'blockquote',
        'div',
        'span',
        'img',
        'figure',
        'figcaption',
        'table',
        'thead',
        'tbody',
        'tr',
        'th',
        'td',
    ]
)

_RICH_TEXT_CSS_PROPERTIES = (
    'text-align',
    'margin',
    'margin-left',
    'margin-right',
    'margin-top',
    'margin-bottom',
    'padding',
    'padding-left',
    'padding-right',
    'width',
    'max-width',
    'height',
    'float',
    'display',
)


def _rich_text_css_sanitizer():
    if CSSSanitizer is None:
        return None
    return CSSSanitizer(allowed_css_properties=_RICH_TEXT_CSS_PROPERTIES)

_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    '*': ['class', 'style', 'align'],
}


def sanitize_rich_html(value: str) -> str:
    if not value:
        return ''
    kwargs = {
        'tags': _ALLOWED_TAGS,
        'attributes': _ALLOWED_ATTRIBUTES,
        'strip': True,
    }
    css = _rich_text_css_sanitizer()
    if css is not None:
        kwargs['css_sanitizer'] = css
    return bleach.clean(str(value), **kwargs)


def sanitize_translated_descriptions(instance, base_field: str = 'description') -> None:
    """Sanitize modeltranslation localized columns, e.g. description_en, description_ru."""
    from django.conf import settings
    from modeltranslation.utils import build_localized_fieldname

    for lang_code, _ in getattr(settings, 'LANGUAGES', ()):
        fname = build_localized_fieldname(base_field, lang_code)
        if hasattr(instance, fname):
            val = getattr(instance, fname)
            if val:
                setattr(instance, fname, sanitize_rich_html(val))
