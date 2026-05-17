"""Serialize country + additional info for public modal and owner edit."""

from django.utils import translation

from .models import AdditionalInformation, Country


def _localized(instance, field: str, lang: str) -> str:
    for code in (lang, 'en', 'ru'):
        val = getattr(instance, f'{field}_{code}', None)
        if val:
            return val
    return getattr(instance, field, '') or ''


def serialize_additional_row(info: AdditionalInformation, lang: str, include_all_langs: bool = False) -> dict:
    row = {
        'id': info.id,
        'key': _localized(info, 'key', lang),
        'value': _localized(info, 'value', lang),
        'order': info.order,
    }
    if include_all_langs:
        row.update(
            {
                'key_en': info.key_en or info.key or '',
                'key_ru': info.key_ru or '',
                'value_en': info.value_en or info.value or '',
                'value_ru': info.value_ru or '',
            }
        )
    return row


def serialize_country(country: Country, user=None, *, for_edit: bool = False) -> dict:
    lang = (translation.get_language() or 'en')[:2]
    owner_id = getattr(country, 'owner_id', None)
    can_edit = bool(
        user
        and user.is_authenticated
        and owner_id is not None
        and owner_id == user.pk
    )

    data = {
        'id': country.id,
        'title': _localized(country, 'title', lang),
        'code': _localized(country, 'code', lang) or country.code or '',
        'description': _localized(country, 'description', lang),
        'href': country.href or '',
        'flag_url': country.flag_url or '',
        'can_edit': can_edit,
        'additional_information': [
            serialize_additional_row(info, lang, include_all_langs=for_edit)
            for info in country.additional_information.all()
        ],
    }

    if for_edit:
        data['description_en'] = country.description_en or country.description or ''
        data['description_ru'] = country.description_ru or ''

    return data
