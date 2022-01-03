from django.core.management.base import BaseCommand
from surveys.models import InvestorCategory


class Command(BaseCommand):
    help = 'Creates the inverter categories to which a user may belong'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing'))
        categories = [
            {"name": "wealth_managements.profiles.conservative", "range_from": 1, "range_to": 7},
            {"name": "wealth_managements.profiles.medium", "range_from": 8, "range_to": 13},
            {"name": "wealth_managements.profiles.risky", "range_from": 14, "range_to": 18}
        ]
        for category in categories:
            InvestorCategory.objects.create(**category)

        self.stdout.write(self.style.SUCCESS('Successful data upload'))
