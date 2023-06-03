import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from orders.models import Order, OrderDelivery, OrderRefund
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


@dataclass
class Notification(ABC):
    request: HttpRequest

    @property
    def message(self):
        pass

    @abstractmethod
    def send(self):
        pass


SMSClient = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@dataclass
class DeliveryMessageNotification(Notification):
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
        content = render_to_string("administration/notifications/sms/" + self.Template[self.delivery.delivery_status].value, {
                                   'order': self.order, 'delivery': self.delivery}, 
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

@dataclass
class DeliveryEmailNotification(Notification):
    order: Order
    delivery: OrderDelivery

    class Template(Enum):
        PROCESSING = "delivery-processing.html"
        SHIPPED = "delivery-shipped.html"
        DELIVERED = "delivery-delivered.html"
        FAILED_DELIVERY = "delivery-failed-delivery.html"
        RETURNED = "delivery-returned.html"
        CANCELLED = "delivery-cancelled.html"

    class Subject(Enum):
        PROCESSING = "Sifarişiniz hazırlanır"
        SHIPPED = "Sifarişiniz yoldadır"
        DELIVERED = "Sifarişiniz çatdırılıb"
        FAILED_DELIVERY = "Sifarişinizin çatdırılması uğursuz oldu"
        RETURNED = "Sifarişiniz geri qaytarıldı"
        CANCELLED = "Sifarişinizin çatdırılması ləğv edildi"
    
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
            msg.send()
        except BadHeaderError:
            raise Exception(_("Email cannot be sent"))


@dataclass
class RefundEmailNotification(Notification):
    order: Order
    refund: OrderRefund

    @property
    def message(self):
        content = render_to_string("administration/notifications/emails/refund.html", {
                                   'order': self.order, 'refund': self.refund}, request=self.request)
        return content

    def send(self):
        try:
            msg = EmailMessage(
                subject="Sifarişinizin ödənişi geri qaytarıldı",
                body=self.message,
                from_email=os.environ.get("COMPANY_EMAIL"),
                to=[self.order.email],
            )
            msg.content_subtype = "html"
            msg.send()
        except BadHeaderError:
            raise Exception(_("Email cannot be sent"))
        
@dataclass
class RefundMessageNotification(Notification):
    order: Order
    refund: OrderRefund
    
    @property
    def message(self):
        content = render_to_string("administration/notifications/sms/refund.html", {
                                   'order': self.order, 'refund': self.refund}, 
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


def sendDeliveryStatusNotification(request: HttpRequest, order: Order, delivery: OrderDelivery):
    try:
        if order.email:
            emailNotification = DeliveryEmailNotification(
                request=request, order=order, delivery=delivery)
            emailNotification.send()
        # messageNotification = DeliveryMessageNotification(
        #     request=request, order=order, delivery=delivery)
        # messageNotification.send()
    except Exception as e:
        raise e
    

def sendRefundNotification(request: HttpRequest, order: Order, refund: OrderRefund):
    try:
        if order.email:
            emailNotification = RefundEmailNotification(
                request=request, order=order, refund=refund)
            emailNotification.send()
        # messageNotification = RefundMessageNotification(
        #     request=request, order=order, refund=refund)
        # messageNotification.send()
    except Exception as e:
        raise e