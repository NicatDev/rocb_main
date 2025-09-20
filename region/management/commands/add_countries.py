from django.core.management.base import BaseCommand
from region.models import Country

class Command(BaseCommand):
    help = "Add countries with Russian titles and codes to the database"

    countries = [
        {"title_en": "Albania", "title_ru": "Албания", "code": "AL", "code_ru": "АЛ"},
        {"title_en": "Andorra", "title_ru": "Андорра", "code": "AD", "code_ru": "АД"},
        {"title_en": "Armenia", "title_ru": "Армения", "code": "AM", "code_ru": "АМ"},
        {"title_en": "Austria", "title_ru": "Австрия", "code": "AT", "code_ru": "АТ"},
        {"title_en": "Azerbaijan", "title_ru": "Азербайджан", "code": "AZ", "code_ru": "АЗ"},
        {"title_en": "Belarus", "title_ru": "Беларусь", "code": "BY", "code_ru": "БY"},
        {"title_en": "Belgium", "title_ru": "Бельгия", "code": "BE", "code_ru": "БЕ"},
        {"title_en": "Bosnia and Herzegovina", "title_ru": "Босния и Герцеговина", "code": "BA", "code_ru": "БА"},
        {"title_en": "Bulgaria", "title_ru": "Болгария", "code": "BG", "code_ru": "БГ"},
        {"title_en": "Croatia", "title_ru": "Хорватия", "code": "HR", "code_ru": "ХР"},
        {"title_en": "Cyprus", "title_ru": "Кипр", "code": "CY", "code_ru": "СY"},
        {"title_en": "Czech Republic", "title_ru": "Чехия", "code": "CZ", "code_ru": "ЧZ"},
        {"title_en": "Denmark", "title_ru": "Дания", "code": "DK", "code_ru": "ДK"},
        {"title_en": "Estonia", "title_ru": "Эстония", "code": "EE", "code_ru": "ЭE"},
        {"title_en": "European Union", "title_ru": "Европейский союз", "code": "EU", "code_ru": "ЕU"},
        {"title_en": "Finland", "title_ru": "Финляндия", "code": "FI", "code_ru": "ФI"},
        {"title_en": "France", "title_ru": "Франция", "code": "FR", "code_ru": "ФR"},
        {"title_en": "Georgia", "title_ru": "Грузия", "code": "GE", "code_ru": "ГE"},
        {"title_en": "Germany", "title_ru": "Германия", "code": "DE", "code_ru": "ДE"},
        {"title_en": "Greece", "title_ru": "Греция", "code": "GR", "code_ru": "ГR"},
        {"title_en": "Hungary", "title_ru": "Венгрия", "code": "HU", "code_ru": "HУ"},
        {"title_en": "Iceland", "title_ru": "Исландия", "code": "IS", "code_ru": "ИС"},
        {"title_en": "Ireland", "title_ru": "Ирландия", "code": "IE", "code_ru": "ИE"},
        {"title_en": "Israel", "title_ru": "Израиль", "code": "IL", "code_ru": "ИЛ"},
        {"title_en": "Italy", "title_ru": "Италия", "code": "IT", "code_ru": "ИТ"},
        {"title_en": "Kazakhstan", "title_ru": "Казахстан", "code": "KZ", "code_ru": "КZ"},
        {"title_en": "Kosovo", "title_ru": "Косово", "code": "XK", "code_ru": "ХK"},
        {"title_en": "Kyrgyz Republic", "title_ru": "Кыргызстан", "code": "KG", "code_ru": "КG"},
        {"title_en": "Latvia", "title_ru": "Латвия", "code": "LV", "code_ru": "ЛV"},
        {"title_en": "Lithuania", "title_ru": "Литва", "code": "LT", "code_ru": "ЛT"},
        {"title_en": "Luxembourg", "title_ru": "Люксембург", "code": "LU", "code_ru": "ЛU"},
        {"title_en": "Malta", "title_ru": "Мальта", "code": "MT", "code_ru": "MТ"},
        {"title_en": "Moldova", "title_ru": "Молдова", "code": "MD", "code_ru": "MД"},
        {"title_en": "Montenegro", "title_ru": "Черногория", "code": "ME", "code_ru": "MЕ"},
        {"title_en": "Netherlands", "title_ru": "Нидерланды", "code": "NL", "code_ru": "НL"},
        {"title_en": "Norway", "title_ru": "Норвегия", "code": "NO", "code_ru": "NО"},
        {"title_en": "Poland", "title_ru": "Польша", "code": "PL", "code_ru": "ПL"},
        {"title_en": "Portugal", "title_ru": "Португалия", "code": "PT", "code_ru": "ПT"},
        {"title_en": "Romania", "title_ru": "Румыния", "code": "RO", "code_ru": "РO"},
        {"title_en": "Russian Federation", "title_ru": "Россия", "code": "RU", "code_ru": "РU"},
        {"title_en": "Serbia", "title_ru": "Сербия", "code": "RS", "code_ru": "СS"},
        {"title_en": "Slovakia", "title_ru": "Словакия", "code": "SK", "code_ru": "СK"},
        {"title_en": "Slovenia", "title_ru": "Словения", "code": "SI", "code_ru": "СI"},
        {"title_en": "Spain", "title_ru": "Испания", "code": "ES", "code_ru": "EС"},
        {"title_en": "Sweden", "title_ru": "Швеция", "code": "SE", "code_ru": "ШE"},
        {"title_en": "Switzerland", "title_ru": "Швейцария", "code": "CH", "code_ru": "CH"},
        {"title_en": "Tajikistan", "title_ru": "Таджикистан", "code": "TJ", "code_ru": "TJ"},
        {"title_en": "North Macedonia", "title_ru": "Северная Македония", "code": "MK", "code_ru": "MК"},
        {"title_en": "Turkey", "title_ru": "Турция", "code": "TR", "code_ru": "TР"},
        {"title_en": "Turkmenistan", "title_ru": "Туркменистан", "code": "TM", "code_ru": "TМ"},
        {"title_en": "Ukraine", "title_ru": "Украина", "code": "UA", "code_ru": "УA"},
        {"title_en": "United Kingdom", "title_ru": "Великобритания", "code": "GB", "code_ru": "ГB"},
        {"title_en": "Uzbekistan", "title_ru": "Узбекистан", "code": "UZ", "code_ru": "УZ"}
    ]

    FLAG_TEMPLATE = "https://flagcdn.com/64x48/{code_lower}.png"

    def handle(self, *args, **kwargs):
        for data in self.countries:
            code = data["code"].lower()
            flag_url = self.FLAG_TEMPLATE.format(code_lower=code)
            obj, created = Country.objects.update_or_create(
                code=data["code"],
                defaults={
                    "title_en": data["title_en"],
                    "title_ru": data["title_ru"],
                    "code_ru": data["code_ru"],
                    "flag_url": flag_url,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added {data["title_en"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated {data["title_en"]}'))