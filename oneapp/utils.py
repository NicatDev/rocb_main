import random
import string

from django.urls import get_resolver

def code_slug_generator(size=12, chars=string.ascii_letters):
    return ''.join(random.choice(chars)
                   for _ in range(size))

def code_generator(size=4, chars=string.ascii_letters):
    return ''.join(random.choice(chars)
                   for _ in range(size))

def create_slug_shortcode(size, model_):
    new_code = code_slug_generator(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    return create_slug_shortcode(size, model_) if qs_exists else new_code


# Azerice slugfy function
def slugify(title):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        ('!', '-'),
        ('?', '-'),
        ("'", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )

    title_url = title.strip().lower()

    for before, after in symbol_mapping:
        title_url = title_url.replace(before, after)

    return title_url


def get_url_names():
    url_names = []
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        if pattern.name:  # Only include named patterns
            url_names.append((pattern.name, pattern.name.replace('_', ' ').title()))
    return url_names
