import json

import requests
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def api_endpoint(method: str) -> str:
    return f"{settings.PAYRIFF_API_ENDPOINT}{method}"


class PaymentGateway:

    @staticmethod
    def charge(request: HttpRequest, description: str, amount: float):
        try:
            data = {
                "body": {
                    "amount": amount,
                    "approveURL": f"{settings.SITE_URL}{reverse('api:checkout-success')}",
                    "cancelURL": f"{settings.SITE_URL}{reverse('api:checkout-cancel')}",
                    "currencyType": "AZN",
                    "declineURL": f"{settings.SITE_URL}{reverse('api:checkout-decline')}",
                    "description": description,
                    "directPay": True,
                    "installmentPeriod": 0,
                    "language": "AZ"
                },
                "merchant": settings.PAYRIFF_MERCHANT
            }

            response = requests.post("https://api.payriff.com/api/v2/createOrder",
                                     data=json.dumps(data),
                                     headers={
                                         "Authorization": settings.PAYRIFF_SECRET_KEY,
                                         "Content-Type": "application/json"}
                                     )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(_("Order failed"))
        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def getOrder(request):
        pass

    @staticmethod
    def refund(request: HttpRequest, amount: float, orderId: int, sessionId: str):
        try:
            data = {
                "body": {
                    "refundAmount": amount,
                    "orderId": orderId,
                    "sessionId": sessionId
                },
                "merchant": settings.PAYRIFF_MERCHANT
            }
            response = requests.post("https://api.payriff.com/api/v2/refund",
                                     data=json.dumps(data),
                                     headers={
                                         "Authorization": settings.PAYRIFF_SECRET_KEY,
                                         "Content-Type": "application/json"}
                                     )            
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()
                raise Exception(_("Refund failed"))
        except Exception as e:
            raise Exception(str(e))
