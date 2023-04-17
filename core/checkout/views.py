import random
import string
from urllib.parse import urlencode

from cart.processor import CartProcessor
from django.contrib import messages
from django.db import DatabaseError, transaction
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods
from orders.forms import OrderForm
from orders.models import Order, OrderItem


def order_key_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@require_http_methods(['GET', 'POST'])
def index(request):
    cart = CartProcessor(request)

    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.total_paid = cart.get_total_price
                    order.order_key = order_key_generator()
                    order.save()

                    for item in cart:
                        OrderItem.objects.create(order_id=order.id, product_id=item['product']['id'], price=item['price'], quantity=item['quantity'])

                    cart.clear()
                    
                    successUrl = '{}?{}'.format(reverse('checkout:success'), urlencode({'order': order.order_key})) 
                    messages.success(request, f'Order was placed successfully')
                    return redirect(successUrl)
            messages.error(request, "Product cannot be saved")
            return render(request, "checkout/index.html", {
                    'cart': cart,
                    'form': form,
                })
        except DatabaseError:
            messages.error(request, "Product cannot be saved")
            return render(request, "checkout/index.html", {
                    'cart': cart,
                    'form': form,
                })
    form = OrderForm()
    return render(request, 'checkout/index.html', context={
        'cart': cart,
        'form': form,
    }) 


@require_GET
def success(request):
    if 'order' not in request.GET:
        return HttpResponseNotFound("Not found")

    try:
        order = Order.objects.prefetch_related('items__product').get(order_key=request.GET.get('order'))
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order not found")
    return render(request, 'checkout/success.html', {"order": order})
     