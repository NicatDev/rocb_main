"""Bulk create/update member country owner users."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.text import slugify

from account.models import Profile
from .models import Country

User = get_user_model()

PASSWORD_SUFFIX = '-123456'


def country_username(title: str, country_id: int | None = None) -> str:
    """Django-safe username from country title."""
    base = slugify(title or '') or f'country-{country_id or 0}'
    base = base[:140]
    return base


def country_password(username: str) -> str:
    return f'{username}{PASSWORD_SUFFIX}'


def _unique_username(base: str, country_id: int) -> str:
    if not User.objects.filter(username=base).exists():
        return base
    candidate = f'{base}-{country_id}'[:150]
    n = 2
    while User.objects.filter(username=candidate).exists():
        candidate = f'{base}-{country_id}-{n}'[:150]
        n += 1
    return candidate


def serialize_country_owner_row(country: Country) -> dict[str, Any]:
    username = country_username(country.title, country.id)
    owner = country.owner
    row = {
        'country_id': country.id,
        'title': country.title,
        'code': country.code,
        'region_id': country.region_id,
        'owner': None,
        'credentials_template': {
            'username': username,
            'password': country_password(username),
        },
    }
    if owner:
        row['owner'] = {
            'user_id': owner.pk,
            'username': owner.username,
            'email': owner.email,
            'is_active': owner.is_active,
        }
    return row


def list_countries_with_owners(
    *,
    region_id: int | None = None,
    country_ids: list[int] | None = None,
    only_unassigned: bool = False,
) -> list[dict[str, Any]]:
    qs = Country.objects.select_related('owner', 'region').order_by('title')
    if region_id is not None:
        qs = qs.filter(region_id=region_id)
    if country_ids:
        qs = qs.filter(pk__in=country_ids)
    if only_unassigned:
        qs = qs.filter(owner__isnull=True)
    return [serialize_country_owner_row(c) for c in qs]


def _ensure_profile(user: User, country_title: str) -> Profile:
    profile, created = Profile.objects.get_or_create(user=user)
    update_fields = []
    if profile.status != 'approved':
        profile.status = 'approved'
        update_fields.append('status')
    if not profile.organization:
        profile.organization = country_title[:100]
        update_fields.append('organization')
    if not profile.position:
        profile.position = 'Member administration owner'
        update_fields.append('position')
    if update_fields:
        profile.save(update_fields=update_fields)
    return profile


def _get_or_create_owner_user(country: Country, *, reset_password: bool) -> tuple[User, bool, bool]:
    """
    Returns (user, created, password_updated).
  """
    base_username = country_username(country.title, country.id)
    username = _unique_username(base_username, country.id)
    password = country_password(base_username)

    existing = User.objects.filter(username=username).first()
    if existing:
        user = existing
        created = False
        if reset_password:
            user.set_password(password)
            user.save(update_fields=['password'])
            password_updated = True
        else:
            password_updated = False
    else:
        email = f'{username}@members.rocbeurope.org'
        if User.objects.filter(email=email).exists():
            email = f'{username}.{country.id}@members.rocbeurope.org'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=country.title[:30],
        )
        created = True
        password_updated = True

    changed_user = False
    if not user.is_active:
        user.is_active = True
        changed_user = True
    if not user.is_staff:
        pass  # members should not be staff
    if changed_user:
        user.save(update_fields=['is_active'])

    _ensure_profile(user, country.title)
    return user, created, password_updated


@transaction.atomic
def bulk_create_country_owners(
    *,
    region_id: int | None = None,
    country_ids: list[int] | None = None,
    only_unassigned: bool = True,
    reset_passwords: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    qs = Country.objects.select_related('owner', 'region').order_by('title')
    if region_id is not None:
        qs = qs.filter(region_id=region_id)
    if country_ids:
        qs = qs.filter(pk__in=country_ids)
    if only_unassigned:
        qs = qs.filter(owner__isnull=True)

    results: list[dict[str, Any]] = []
    created_users = 0
    linked = 0
    skipped = 0
    passwords_reset = 0

    for country in qs:
        template_username = country_username(country.title, country.id)
        template_password = country_password(template_username)

        if country.owner_id and not reset_passwords:
            results.append({
                'country_id': country.id,
                'title': country.title,
                'status': 'skipped',
                'reason': 'already_has_owner',
                'owner_user_id': country.owner_id,
                'username': country.owner.username,
            })
            skipped += 1
            continue

        if country.owner_id and reset_passwords and not dry_run:
            user = country.owner
            base = country_username(country.title, country.id)
            user.set_password(country_password(base))
            user.is_active = True
            user.save(update_fields=['password', 'is_active'])
            _ensure_profile(user, country.title)
            passwords_reset += 1
            results.append({
                'country_id': country.id,
                'title': country.title,
                'status': 'password_reset',
                'user_id': user.pk,
                'username': user.username,
                'password': country_password(base),
            })
            continue

        if country.owner_id and reset_passwords and dry_run:
            base = country_username(country.title, country.id)
            results.append({
                'country_id': country.id,
                'title': country.title,
                'status': 'would_reset_password',
                'owner_user_id': country.owner_id,
                'password': country_password(base),
            })
            continue

        if dry_run:
            results.append({
                'country_id': country.id,
                'title': country.title,
                'status': 'would_create',
                'username': template_username,
                'password': template_password,
            })
            continue

        user, created, pwd_updated = _get_or_create_owner_user(
            country, reset_password=reset_passwords
        )
        if created:
            created_users += 1
        if pwd_updated:
            passwords_reset += 1

        country.owner = user
        country.save(update_fields=['owner'])
        linked += 1

        results.append({
            'country_id': country.id,
            'title': country.title,
            'status': 'created' if created else 'linked',
            'user_id': user.pk,
            'username': user.username,
            'password': template_password if (created or reset_passwords) else None,
        })

    return {
        'dry_run': dry_run,
        'summary': {
            'processed': len(results),
            'created_users': created_users,
            'linked': linked,
            'skipped': skipped,
            'passwords_reset': passwords_reset,
        },
        'results': results,
    }


@transaction.atomic
def bulk_update_country_owners(
    items: list[dict[str, Any]],
    *,
    reset_passwords: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    items: [{country_id, user_id?}, {country_id, username?}, {country_id, clear_owner?}]
    """
    results = []
    updated = 0

    for item in items:
        country_id = item.get('country_id')
        if not country_id:
            results.append({'status': 'error', 'error': 'country_id required'})
            continue

        try:
            country = Country.objects.select_related('owner').get(pk=country_id)
        except Country.DoesNotExist:
            results.append({'country_id': country_id, 'status': 'error', 'error': 'not_found'})
            continue

        if item.get('clear_owner'):
            if dry_run:
                results.append({'country_id': country_id, 'status': 'would_clear_owner'})
                continue
            country.owner = None
            country.save(update_fields=['owner'])
            results.append({'country_id': country_id, 'status': 'cleared_owner'})
            updated += 1
            continue

        user_id = item.get('user_id')
        username = item.get('username')
        user = None
        if user_id:
            user = User.objects.filter(pk=user_id).first()
        elif username:
            user = User.objects.filter(username=username).first()

        if not user:
            results.append({
                'country_id': country_id,
                'status': 'error',
                'error': 'user_not_found',
            })
            continue

        if dry_run:
            results.append({
                'country_id': country_id,
                'status': 'would_assign',
                'user_id': user.pk,
                'username': user.username,
            })
            continue

        if reset_passwords:
            base = country_username(country.title, country.id)
            user.set_password(country_password(base))
            user.save(update_fields=['password'])

        country.owner = user
        country.save(update_fields=['owner'])
        _ensure_profile(user, country.title)
        results.append({
            'country_id': country_id,
            'status': 'assigned',
            'user_id': user.pk,
            'username': user.username,
        })
        updated += 1

    return {
        'dry_run': dry_run,
        'summary': {'updated': updated, 'items': len(items)},
        'results': results,
    }
