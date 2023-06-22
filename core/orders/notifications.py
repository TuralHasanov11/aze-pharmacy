from enum import Enum

from api.serializers import OrderNotificationSerializer
from django.utils.translation import gettext_lazy as _
from orders.models import Order

from core.broadcast import BroadcastChannel


class OrderCreatedEvent:
    channel_name: str = 'orders'
    event_name: str = "created"
    order: Order

    def __init__(self, order: Order):
        self.order = order

    def dispatch(self):
        return BroadcastChannel(
            channel_name=self.channel_name,
            event_name=self.event_name,
            payload={
                "message": _("New order: ") + f" {self.order.id}",
                "data": OrderNotificationSerializer(self.order).data
            })
