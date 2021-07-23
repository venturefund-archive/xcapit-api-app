from api_app import settings


class MercadopagoURL:
    def __init__(self, path: str, api_url=settings.API_MERCADOPAGO):
        self._path = path
        self._api_url = api_url

    def __str__(self):
        return f'{self._api_url}{self._path}'
