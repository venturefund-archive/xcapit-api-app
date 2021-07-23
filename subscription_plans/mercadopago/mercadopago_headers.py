from api_app import settings


class DefaultMercadopagoHeaders:
    def value(self):
        return {
            'Authorization': f'Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
