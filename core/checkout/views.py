import json
import random
import string
from urllib.parse import urlencode

from administration.notifications import sendDeliveryStatusNotification
from api import serializers
from asgiref.sync import async_to_sync
from cart.processor import CartProcessor
from channels.layers import get_channel_layer
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods
from orders.forms import OrderForm
from orders.models import Order, OrderDelivery, OrderItem


def order_key_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@require_http_methods(['GET', 'POST'])
def index(request):
    cart = CartProcessor(request)
    breadcrumb = [
        {"title": _("Checkout")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Checkout")},
    ]
    template_name = "checkout/index.html"
    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            if form.is_valid():
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.send)("orders", {
                    "type": "order_created",
                    "message": "order was",
                })
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.total_paid = cart.get_total_price
                    order.order_key = order_key_generator()
                    order.payment_status = order.PaymentStatus.PAID
                    order.save()

                    for item in cart:
                        OrderItem.objects.create(
                            order_id=order.id,
                            product_id=item['product']['id'],
                            price=item['price'],
                            sub_total=item['total_price'],
                            quantity=item['quantity']
                        )

                    delivery = OrderDelivery.objects.create(order=order)
                    order = Order.objects.select_related('order_delivery').prefetch_related(
                        Prefetch('items', queryset=OrderItem.objects.select_related(
                            'product__category').all()),
                    ).get(id=order.id)
                    
                    sendDeliveryStatusNotification(
                            request=request, order=order, delivery=delivery)
                    
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)("orders", {
                        "type": "order_created",
                        "message": "new order",
                    })

                    cart.clear()
                    successUrl = f"{reverse('orders:detail', kwargs={'id': order.id})}?{urlencode({'order_key': order.order_key})}#order-summary"
                    messages.success(request, _(
                        'Order was placed successfully'))
                    return JsonResponse(data={"success_url": successUrl})
            return JsonResponse(status=422, data={"message": _("Order cannot be placed"), "errors": json.dumps(form.errors)})
        except Exception as e:
            return JsonResponse(status=400, data={"message": _("Order cannot be placed"), "errors": str(e)})
    form = OrderForm()
    return render(request, template_name, context={
        'cart': cart,
        'form': form,
        "breadcrumb": breadcrumb
    })
