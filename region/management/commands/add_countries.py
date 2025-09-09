from django.core.management.base import BaseCommand
from region.models import Country

class Command(BaseCommand):
    help = "Add countries to the database"

    countries = [
        {"title": "Albania", "code": "AL"},
        {"title": "Andorra", "code": "AD"},
        {"title": "Armenia", "code": "AM"},
        {"title": "Austria", "code": "AT"},
        {"title": "Azerbaijan", "code": "AZ"},
        {"title": "Belarus", "code": "BY"},
        {"title": "Belgium", "code": "BE"},
        {"title": "Bosnia and Herzegovina", "code": "BA"},
        {"title": "Bulgaria", "code": "BG"},
        {"title": "Croatia", "code": "HR"},
        {"title": "Cyprus", "code": "CY"},
        {"title": "Czech Republic", "code": "CZ"},
        {"title": "Denmark", "code": "DK"},
        {"title": "Estonia", "code": "EE"},
        {"title": "European Union", "code": "EU"},
        {"title": "Finland", "code": "FI"},
        {"title": "France", "code": "FR"},
        {"title": "Georgia", "code": "GE"},
        {"title": "Germany", "code": "DE"},
        {"title": "Greece", "code": "GR"},
        {"title": "Hungary", "code": "HU"},
        {"title": "Iceland", "code": "IS"},
        {"title": "Ireland", "code": "IE"},
        {"title": "Israel", "code": "IL"},
        {"title": "Italy", "code": "IT"},
        {"title": "Kazakhstan", "code": "KZ"},
        {"title": "Kosovo", "code": "XK"},
        {"title": "Kyrgyz Republic", "code": "KG"},
        {"title": "Latvia", "code": "LV"},
        {"title": "Lithuania", "code": "LT"},
        {"title": "Luxembourg", "code": "LU"},
        {"title": "Malta", "code": "MT"},
        {"title": "Moldova", "code": "MD"},
        {"title": "Montenegro", "code": "ME"},
        {"title": "Netherlands", "code": "NL"},
        {"title": "Norway", "code": "NO"},
        {"title": "Poland", "code": "PL"},
        {"title": "Portugal", "code": "PT"},
        {"title": "Romania", "code": "RO"},
        {"title": "Russian Federation", "code": "RU"},
        {"title": "Serbia", "code": "RS"},
        {"title": "Slovakia", "code": "SK"},
        {"title": "Slovenia", "code": "SI"},
        {"title": "Spain", "code": "ES"},
        {"title": "Sweden", "code": "SE"},
        {"title": "Switzerland", "code": "CH"},
        {"title": "Tajikistan", "code": "TJ"},
        {"title": "North Macedonia", "code": "MK"},
        {"title": "Turkey", "code": "TR"},
        {"title": "Turkmenistan", "code": "TM"},
        {"title": "Ukraine", "code": "UA"},
        {"title": "United Kingdom", "code": "GB"},
        {"title": "Uzbekistan", "code": "UZ"}
    ]

    def handle(self, *args, **kwargs):
        for country in self.countries:
            obj, created = Country.objects.get_or_create(
                code=country["code"],
                defaults={"title": country["title"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added {country["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'{country["title"]} already exists'))