"""
Fetch global public news from rocb_app_news (app.rocbeurope.org API).
"""
import logging
import re
from html import unescape
from urllib.parse import quote

import requests
from typing import Optional, Tuple

from django.conf import settings
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)


def _media_origin() -> str:
    base = getattr(settings, 'RTC_APP_NEWS_API_BASE', 'https://app.rocbeurope.org/api/v1').rstrip('/')
    if '/api' in base:
        return base.split('/api')[0].rstrip('/') or 'https://app.rocbeurope.org'
    return 'https://app.rocbeurope.org'


def _strip_html(value) -> str:
    if not value:
        return ''
    text = unescape(re.sub(r'<[^>]+>', ' ', str(value)))
    return ' '.join(text.split())


def _abs_media_url(url) -> Optional[str]:
    if not url:
        return None
    u = str(url).strip()
    if u.startswith('http://') or u.startswith('https://'):
        return u
    origin = _media_origin()
    path = u if u.startswith('/') else f'/{u}'
    return f'{origin}{path}'


class _Image:
    def __init__(self, url: str | None):
        self.url = url


class _EmptyNewsSections:
    def all(self):
        return []


class ApiNewsItem:
    """Maps API payload to attributes used by rocb_main templates."""

    def __init__(self, data: dict, *, for_detail: bool = False):
        self.id = data.get('id')
        self.slug = data.get('slug') or ''
        self.title = data.get('title') or ''
        raw_content = data.get('content') or ''
        self.content = raw_content if for_detail else None
        plain = _strip_html(raw_content)
        self.description = plain[:2000] if plain else ''
        img = _abs_media_url(data.get('image'))
        self.image = _Image(img) if img else None
        self.tag = ''
        created = data.get('created_at')
        dt = parse_datetime(created) if created else None
        self.date = dt
        self.created_by = None
        self.autorized_image = None
        self.news_sections = _EmptyNewsSections()


def _list_url() -> str:
    base = getattr(settings, 'RTC_APP_NEWS_API_BASE', 'https://app.rocbeurope.org/api/v1').rstrip('/')
    return f'{base}/public/main-site/news/'


def fetch_main_site_news_page(page: int = 1, page_size: int = 8, search: Optional[str] = None) -> Optional[dict]:
    params = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    try:
        r = requests.get(_list_url(), params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        logger.exception('Failed to fetch main-site news: %s', exc)
        return None


def fetch_main_site_news_detail(slug: str) -> Optional[dict]:
    base = getattr(settings, 'RTC_APP_NEWS_API_BASE', 'https://app.rocbeurope.org/api/v1').rstrip('/')
    url = f'{base}/public/main-site/news/{quote(slug, safe="")}/'
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        logger.exception('Failed to fetch news detail %s: %s', slug, exc)
        return None


def fetch_main_site_news_batch(page_size: int = 8) -> Optional[dict]:
    return fetch_main_site_news_page(page=1, page_size=page_size, search=None)


def prev_next_slugs(current_slug: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Ordering is -created_at (newest first). Prev = older, next = newer.
    """
    data = fetch_main_site_news_page(page=1, page_size=100, search=None)
    if not data or 'results' not in data:
        return None, None
    slugs = [row.get('slug') for row in data['results'] if row.get('slug')]
    try:
        idx = slugs.index(current_slug)
    except ValueError:
        return None, None
    prev_slug = slugs[idx + 1] if idx + 1 < len(slugs) else None
    next_slug = slugs[idx - 1] if idx > 0 else None
    return prev_slug, next_slug


class RemotePaginator:
    def __init__(self, count: int, per_page: int):
        self.count = count
        self.per_page = per_page
        self.num_pages = max(1, (count + per_page - 1) // per_page) if count else 1
        self.page_range = range(1, self.num_pages + 1)


class RemotePage:
    def __init__(self, object_list, number: int, paginator: RemotePaginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __iter__(self):
        return iter(self.object_list)

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def next_page_number(self):
        return self.number + 1

    def previous_page_number(self):
        return self.number - 1


def build_page_from_api(data: Optional[dict], page_number: int, page_size: int):
    if not data:
        paginator = RemotePaginator(0, page_size)
        return RemotePage([], max(1, page_number), paginator)
    total = data.get('count', 0)
    results = [ApiNewsItem(row, for_detail=False) for row in data.get('results', [])]
    paginator = RemotePaginator(total, page_size)
    return RemotePage(results, page_number, paginator)


class SlugRef:
    __slots__ = ('slug',)

    def __init__(self, slug: str):
        self.slug = slug


def discover_tabs_excluding(page_obj, limit: int = 3):
    """Sidebar 'Discover More' links — latest global news not on the current page."""
    data = fetch_main_site_news_page(1, page_size=16)
    if not data:
        return []
    on_page = {getattr(x, 'slug', None) for x in page_obj.object_list}
    tabs = []
    for row in data.get('results', []):
        slug = row.get('slug')
        if not slug or slug in on_page:
            continue
        tabs.append(ApiNewsItem(row, for_detail=False))
        if len(tabs) >= limit:
            break
    return tabs


def search_news_rows(query: str):
    """Dict rows compatible with search_results.html (News type)."""
    data = fetch_main_site_news_page(1, page_size=50, search=query)
    if not data:
        return []
    rows = []
    for row in data.get('results', []):
        item = ApiNewsItem(row, for_detail=False)
        rows.append({
            'title': item.title,
            'description': item.description,
            'image': item.image,
            'date': item.date,
            'slug': item.slug,
            'type': 'News',
        })
    return rows
