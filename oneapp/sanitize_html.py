"""Server-side HTML cleanup for rich-text fields (CKEditor / admin)."""

import bleach

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

_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    '*': ['class'],
}


def sanitize_rich_html(value: str) -> str:
    if not value:
        return ''
    return bleach.clean(
        str(value),
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        strip=True,
    )


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
