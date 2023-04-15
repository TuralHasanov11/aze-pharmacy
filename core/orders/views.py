import json

from cart.processor import CartProcessor
from checkout import payment
from django.contrib.auth import decorators as authDecorators
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.views.decorators import http
from django.views.decorators.http import require_POST
from orders.forms import OrderForm
from orders.models import Order, OrderItem


@login_required
@require_POST
def add(request):
     
    form = OrderForm(request.POST) 
    
    if form.is_valid():
        cart = CartProcessor(request)
        data = form.cleaned_data
        cartTotal = cart.get_total_price
        try:
            if not Order.objects.filter(order_key=data["order_key"]).exists():
                order = Order.objects.create(
                    user=request.user, 
                    full_name=data["full_name"], 
                    address1=data["address1"], 
                    address2=data["address2"], 
                    total_paid=cartTotal, 
                    order_key=data["order_key"],
                    email=data["email"] or request.user.email,
                    city=data["city"],
                    phone=data["phone"],
                    postal_code=data["postal_code"],
                    country_code=data["country_code"],
                    payment_option=payment.PaymentOptions.CARD,
                )

                for item in cart:
                    OrderItem.objects.create(order_id=order.id, product=item['product'], price=item['price'], quantity=item['quantity'])

                return JsonResponse({"order_id": order.id})
        except Exception as err:
            print(err)
            return HttpResponseBadRequest(json.dumps(err)) 
        return JsonResponse({'success': 'Order has been set'})
    else:
        return JsonResponse(form.errors, status=400) 