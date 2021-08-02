from subscription_plans.models import PlanModel
from django.core.management.base import BaseCommand
from subscription_plans.models import PaymentMethodModel


class Command(BaseCommand):
    help = 'Create a free plan model and payment method mercadopago'

    def add_arguments(self, parser):
        parser.add_argument('--paid_plan_price', type=int, required=True)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🤞Starting'))
        paid_plan_price = options.get('paid_plan_price')
        free_plan = PlanModel(
            name='Explorer',
            info='payment.licenses.infoExplorer',
            price='payment.licenses.free',
            type='free',
            frequency=1,
            frequency_type='months'
        )
        free_plan.save()
        paid_plan = PlanModel(
            name='Advanced',
            info='payment.licenses.infoAdvanced',
            price=paid_plan_price,
            type='paid',
            frequency=1,
            frequency_type='months'
        )
        paid_plan.save()

        pmm = PaymentMethodModel(name='Mercadopago', description='Argentina')
        pmm.save()

        self.stdout.write(self.style.SUCCESS('🥳 Success'))
