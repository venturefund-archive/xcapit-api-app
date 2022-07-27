from django.core.management.base import BaseCommand
from wallets.models import Wallet


class Command(BaseCommand):
    help = 'Migrate existing wallets address to user address field model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'🤞Starting.. {Wallet.objects.filter(network="ERC20").count()} wallets'))
        for wallet in Wallet.objects.filter(network='ERC20'):
            wallet.user.address = wallet.address
            wallet.user.save()
        self.stdout.write(self.style.SUCCESS('🥳 Success'))
