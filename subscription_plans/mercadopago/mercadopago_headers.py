from api_app import settings
from core.http.request_headers import RequestHeaders


class DefaultMercadopagoHeaders(RequestHeaders):
    def value(self):
        return {
            'Authorization': f'Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
