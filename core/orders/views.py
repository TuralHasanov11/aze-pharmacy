import json

from cart.processor import CartProcessor
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from store.models import ProductImage


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
                )

                for item in cart:
                    OrderItem.objects.create(
                        order_id=order.id, product=item['product'], price=item['price'], quantity=item['quantity'])

                return JsonResponse({"order_id": order.id})
        except Exception as err:
            print(err)
            return HttpResponseBadRequest(json.dumps(err))
        return JsonResponse({'success': 'Order has been set'})
    else:
        return JsonResponse(form.errors, status=400)


@require_GET
def detail(request, id: int):
    order = Order.objects.select_related('order_delivery').prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product__category').prefetch_related(
                Prefetch("product__product_image", queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature') 
            ).all()),
        ).get(id=id, order_key=request.GET.get('order_key'))
    
    order_quantity = sum([item.quantity for item in order.items.all()])
    
    breadcrumb = [
        {"title": _("Order Details")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Order Details")},
    ]
    
    return render(request, 'orders/detail.html', context={'order': order, "breadcrumb": breadcrumb, "order_quantity": order_quantity})