import json
from enum import Enum

import requests
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class PaymentGateway:
    class PaymentStatus(Enum):
        PAID = "APPROVED"
        PENDING = "CREATED"
        FAILED = "DECLINED"

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

            response = requests.post(f"{settings.PAYRIFF_API_ENDPOINT}createOrder",
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
            raise e

    @staticmethod
    def isPaid(request: HttpRequest, orderId: int, orderKey: str):
        order = PaymentGateway.getOrderDetails(request, orderId, orderKey)
        if order["orderstatus"] == PaymentGateway.PaymentStatus.PAID.value:
            return True
        return False

    @staticmethod
    def getOrderDetails(request: HttpRequest, orderId: int, orderKey: str):
        try:
            data = {
                "body": {
                    "orderId": orderId,
                    "sessionId": orderKey,
                    "languageType": "AZ"
                },
                "merchant": settings.PAYRIFF_MERCHANT
            }

            response = requests.post(f"{settings.PAYRIFF_API_ENDPOINT}getOrderInformation",
                                     data=json.dumps(data),
                                     headers={
                                         "Authorization": settings.PAYRIFF_SECRET_KEY,
                                         "Content-Type": "application/json"}
                                     )
            if response.status_code == 200:
                return response.json()["payload"]["row"]
            else:
                raise Exception(_("Order not found"))
        except Exception as e:
            raise e

    @staticmethod
    def refund(request: HttpRequest, amount: float, orderId: int, orderKey: str):
        try:
            data = {
                "body": {
                    "refundAmount": amount,
                    "orderId": orderId,
                    "sessionId": orderKey
                },
                "merchant": settings.PAYRIFF_MERCHANT
            }
            response = requests.post(f"{settings.PAYRIFF_API_ENDPOINT}refund",
                                     data=json.dumps(data),
                                     headers={
                                         "Authorization": settings.PAYRIFF_SECRET_KEY,
                                         "Content-Type": "application/json"}
                                     )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(_("Refund failed"))
        except Exception as e:
            raise Exception(str(e))
