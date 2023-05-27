import http.client
import json
from decimal import Decimal

import requests
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse


def api_endpoint(method: str) -> str:
    return f"{settings.PAYRIFF_API_ENDPOINT}{method}"
class PaymentGateway:

    @staticmethod
    def charge(request: HttpRequest, description: str, amount):
        try:
            data = {
                "body": {
                    "amount": 11,
                    "approveURL": "http://127.0.0.1:8000/api/checkout/approve-payment/",
                    "cancelURL": "http://127.0.0.1:8000/api/checkout/cancel-payment/",
                    "currencyType": "AZN",
                    "declineURL": "http://127.0.0.1:8000/api/checkout/decline-payment/",
                    "description": "string",
                    "directPay": True,
                    "installmentPeriod": 0,
                    "language": "AZ"
                },
                "merchant": "ES1091902"
            }
            # conn = http.client.HTTPSConnection('api.payriff.com') 
            # conn.request(
            #     method='POST', 
            #     url="api/v2/createOrder",
            #     body=json.dumps(data), 
            #     headers={"Authorization": settings.PAYRIFF_SECRET_KEY}
            # )
            # response = conn.getresponse()
            # print(json.dumps(data))
            # conn.close()
            # return json.loads(response.read())

            response = requests.post("https://api.payriff.com/api/v2/createOrder", 
                                     data=str(data), 
                                     headers={"Authorization": settings.PAYRIFF_SECRET_KEY}
                                )
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print(str(e))
            raise e
        
    
    @staticmethod
    def refund(request):
        pass


    @staticmethod
    def getOrder(request):
        pass

    @staticmethod
    def refund(request: HttpRequest, amount: float, orderId:int, sessionId: str):
        try:
            data =  {
                "body": {
                    "refundAmount": amount,
                    "orderId": orderId,
                    "sessionId": sessionId
                },
                "merchant": settings.PAYRIFF_MERCHANT
            }
            response = requests.post("https://api.payriff.com/api/v2/createOrder", 
                                     data=str(data), 
                                     headers={"Authorization": settings.PAYRIFF_SECRET_KEY}
                                )
            print(response.status_code)
            print(response.text)
            return response.json()
        except Exception as e:
            raise Exception(str(e))