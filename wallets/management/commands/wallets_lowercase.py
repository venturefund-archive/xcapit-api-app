from django.core.management import BaseCommand

from wallets.models import Wallet


class Command(BaseCommand):
    help = 'Set wallets to lowercase'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(f'🤞Starting.. {Wallet.objects.exclude(network="SOLANA").count()} wallets'))
        for wallet in Wallet.objects.exclude(network="SOLANA"):
            lowercase_address = wallet.address.lower()
            wallet.address = lowercase_address
            wallet.save()
            if wallet.network == 'ERC20':
                wallet.user.address = lowercase_address
                wallet.user.save()
        self.stdout.write(self.style.SUCCESS('🥳 Success'))
