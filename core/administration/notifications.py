import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from orders.models import Order, OrderDelivery
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


@dataclass
class DeliveryNotification(ABC):
    request: HttpRequest
    order: Order
    delivery: OrderDelivery

    class Template(Enum):
        PROCESSING = "delivery-processing.html"
        SHIPPED = "delivery-shipped.html"
        DELIVERED = "delivery-delivered.html"
        FAILED_DELIVERY = "delivery-failed-delivery.html"
        RETURNED = "delivery-returned.html"
        CANCELLED = "delivery-cancelled.html"

    @property
    def message(self):
        pass

    @abstractmethod
    def send(self):
        pass


SMSClient = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


class DeliveryMessageNotification(DeliveryNotification):
    @property
    def message(self):
        content = render_to_string("administration/notifications/sms/" + self.Template[self.delivery.delivery_status].value, {
                                   'customer_name': self.order.full_name, 'delivery_date': self.delivery.delivery_date.strftime('%d.%m.%y')}, 
                                   request=self.request)
        return content

    def send(self):
        if self.message is not None:
            try:
                SMSClient.messages.create(
                    body=self.message,
                    from_=settings.TWILIO_PHONE,
                    to=self.order.phone
                )
            except TwilioRestException:
                raise Exception(_("SMS cannot be sent"))


class DeliveryEmailNotification(DeliveryNotification):
    class Subject(Enum):
        PROCESSING = "Processing"
        SHIPPED = "SHIPPED"
        DELIVERED = "DELIVERED"
        FAILED_DELIVERY = "FAILED_DELIVERY"
        RETURNED = "RETURNED"
        CANCELLED = "CANCELLED"
    
    @property
    def subject(self):
        return self.Subject[self.delivery.delivery_status].value

    @property
    def message(self):
        content = render_to_string("administration/notifications/emails/" + self.Template[self.delivery.delivery_status].value, {
                                   'order': self.order, 'delivery': self.delivery, }, request=self.request)
        return content

    def send(self):
        try:
            msg = EmailMessage(
                subject=self.subject,
                body=self.message,
                from_email=os.environ.get("COMPANY_EMAIL"),
                to=[self.order.email],
            )
            msg.content_subtype = "html"
            msg.send(fail_silently=True)
        except BadHeaderError:
            raise Exception(_("Email cannot be sent"))
