from subscription_plans.mercadopago.mercadopago_payment_request import MercadopagoPaymentRequest


class PayerEmail:
    def __init__(self, mercadopago_payment_request: MercadopagoPaymentRequest):
        self._mercadopago_payment_request = mercadopago_payment_request

    def value(self):
        return self._mercadopago_payment_request.response().json().get('payer_email')
