"""Create member owner users for all countries (username=slug(title), password=slug-123456)."""

from django.core.management.base import BaseCommand

from region.country_owner_bulk import bulk_create_country_owners, list_countries_with_owners


class Command(BaseCommand):
    help = (
        'Create/login users for each country and assign as Country.owner. '
        'Username: slugified country name. Password: {username}-123456'
    )

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Preview only')
        parser.add_argument(
            '--all',
            action='store_true',
            help='Include countries that already have an owner',
        )
        parser.add_argument('--region-id', type=int, default=None)
        parser.add_argument('--reset-passwords', action='store_true')
        parser.add_argument('--list-only', action='store_true', help='Print countries with IDs')

    def handle(self, *args, **options):
        if options['list_only']:
            rows = list_countries_with_owners(region_id=options['region_id'])
            self.stdout.write(f'Countries: {len(rows)}')
            for row in rows:
                owner = row['owner']
                owner_txt = f"owner={owner['username']} (id={owner['user_id']})" if owner else 'no owner'
                cred = row['credentials_template']
                self.stdout.write(
                    f"  [{row['country_id']}] {row['title']}: {owner_txt} "
                    f"-> {cred['username']} / {cred['password']}"
                )
            return

        result = bulk_create_country_owners(
            region_id=options['region_id'],
            only_unassigned=not options['all'],
            reset_passwords=options['reset_passwords'],
            dry_run=options['dry_run'],
        )
        summary = result['summary']
        self.stdout.write(self.style.SUCCESS(
            f"processed={summary['processed']} created_users={summary['created_users']} "
            f"linked={summary['linked']} skipped={summary['skipped']} dry_run={result['dry_run']}"
        ))
        for row in result['results'][:20]:
            self.stdout.write(f"  {row}")
        if len(result['results']) > 20:
            self.stdout.write(f"  ... and {len(result['results']) - 20} more")
