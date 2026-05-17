"""Staff API: bulk country member owners (list / create / update)."""

from __future__ import annotations

import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .country_owner_bulk import (
    bulk_create_country_owners,
    bulk_update_country_owners,
    list_countries_with_owners,
)


def _staff_or_api_key(request) -> bool:
    if getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False):
        return True
    expected = getattr(settings, 'COUNTRY_OWNER_BULK_API_KEY', '') or ''
    if not expected:
        return False
    provided = request.headers.get('X-Country-Owner-Api-Key', '')
    return provided == expected


def _require_staff_api(view):
    @csrf_exempt
    def wrapped(request, *args, **kwargs):
        if not _staff_or_api_key(request):
            return JsonResponse(
                {'success': False, 'error': 'forbidden', 'message': 'Staff login or valid API key required.'},
                status=403,
            )
        return view(request, *args, **kwargs)

    return wrapped


def _parse_json_body(request) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


@require_GET
@_require_staff_api
def country_owners_list(request):
    """
    GET /api/region/country-owners/
    Query: region_id, only_unassigned=1, country_ids=1,2,3
    """
    region_id = request.GET.get('region_id')
    country_ids_raw = request.GET.get('country_ids', '')
    only_unassigned = request.GET.get('only_unassigned', '').lower() in ('1', 'true', 'yes')

    country_ids = None
    if country_ids_raw:
        try:
            country_ids = [int(x.strip()) for x in country_ids_raw.split(',') if x.strip()]
        except ValueError:
            return JsonResponse({'success': False, 'error': 'invalid country_ids'}, status=400)

    region_id_int = None
    if region_id:
        try:
            region_id_int = int(region_id)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'invalid region_id'}, status=400)

    rows = list_countries_with_owners(
        region_id=region_id_int,
        country_ids=country_ids,
        only_unassigned=only_unassigned,
    )
    return JsonResponse({
        'success': True,
        'count': len(rows),
        'countries': rows,
    })


@require_http_methods(['POST'])
@_require_staff_api
def country_owners_bulk_create(request):
    """
    POST /api/region/country-owners/bulk-create/
    Body: { dry_run, only_unassigned, region_id, country_ids, reset_passwords }
    """
    data = _parse_json_body(request)
    country_ids = data.get('country_ids')
    if country_ids is not None and not isinstance(country_ids, list):
        return JsonResponse({'success': False, 'error': 'country_ids must be a list'}, status=400)

    region_id = data.get('region_id')
    if region_id is not None:
        try:
            region_id = int(region_id)
        except (TypeError, ValueError):
            return JsonResponse({'success': False, 'error': 'invalid region_id'}, status=400)

    payload = bulk_create_country_owners(
        region_id=region_id,
        country_ids=country_ids,
        only_unassigned=data.get('only_unassigned', True),
        reset_passwords=bool(data.get('reset_passwords', False)),
        dry_run=bool(data.get('dry_run', False)),
    )
    return JsonResponse({'success': True, **payload})


@require_http_methods(['PUT', 'PATCH'])
@_require_staff_api
def country_owners_bulk_update(request):
    """
    PUT/PATCH /api/region/country-owners/bulk-update/
    Body: { items: [{country_id, user_id?|username?|clear_owner?}], reset_passwords, dry_run }
    """
    data = _parse_json_body(request)
    items = data.get('items')
    if not isinstance(items, list):
        return JsonResponse({'success': False, 'error': 'items must be a list'}, status=400)

    payload = bulk_update_country_owners(
        items,
        reset_passwords=bool(data.get('reset_passwords', False)),
        dry_run=bool(data.get('dry_run', False)),
    )
    return JsonResponse({'success': True, **payload})
