from django.urls import path

from . import country_owner_api_views

urlpatterns = [
    path(
        'country-owners/',
        country_owner_api_views.country_owners_list,
        name='country_owners_list',
    ),
    path(
        'country-owners/bulk-create/',
        country_owner_api_views.country_owners_bulk_create,
        name='country_owners_bulk_create',
    ),
    path(
        'country-owners/bulk-update/',
        country_owner_api_views.country_owners_bulk_update,
        name='country_owners_bulk_update',
    ),
]
