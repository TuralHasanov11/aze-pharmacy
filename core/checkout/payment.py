from django.conf import settings


class PaymentGateway:
    def card_save(self):
        data = {
            "body": {
                "amount": 4,
                "approveURL": "https://payriff.com/approve",
                "cancelURL": "https://payriff.com/cancel",
                "declineURL": "https://payriff.com/decline",
                "currencyType": "AZN",
                "description": "Card save description",
                "directPay": True,
                "language": "AZ"
            },
            "merchant": "ES10901XX"
        }

    @property
    def api_endpoint(self, method: str):
        return f"{settings.PAYRIFF_API_ENDPOINT}{method}"