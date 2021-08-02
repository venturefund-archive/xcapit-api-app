from subscription_plans.models import PlanModel
from django.core.management.base import BaseCommand
from subscription_plans.models import PaymentMethodModel


class Command(BaseCommand):
    help = 'Create a free plan model and payment methods if does not exists'

    def add_arguments(self, parser):
        parser.add_argument('--paid_plan_price', type=int, required=True)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🤞Starting'))
        paid_plan_price = options.get('paid_plan_price')
        PlanModel.objects.get_or_create(
            name='Explorer',
            info='payment.licenses.infoExplorer',
            price='payment.licenses.free',
            type='free',
            frequency=1,
            frequency_type='months'
        )

        PlanModel.objects.get_or_create(
            name='Advanced',
            info='payment.licenses.infoAdvanced',
            price=paid_plan_price,
            type='paid',
            frequency=1,
            frequency_type='months'
        )
        payment_method_models_data = [
            {
                'name': 'MercadoPago',
                'description': 'payment.methods.arg',
                'status': 'active'
            },
            {
                'name': 'PayPal',
                'description': 'payment.methods.all_countries',
                'status': 'soon'
            },
            {
                'name': 'BitPay',
                'description': 'payment.methods.all_countries',
                'status': 'soon'
            },
            {
                'name': 'Binance',
                'description': 'payment.methods.all_countries',
                'status': 'soon'
            },
        ]
        for data in payment_method_models_data:
            PaymentMethodModel.objects.get_or_create(**data)

        self.stdout.write(self.style.SUCCESS('🥳 Success'))
