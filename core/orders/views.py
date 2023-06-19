from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from orders.models import Order, OrderItem
from store.models import ProductImage


@require_GET
def detail(request, id: int):
    try:
        order = Order.objects.select_related('order_delivery').prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product__category').prefetch_related(
                Prefetch("product__product_image", queryset=ProductImage.objects.filter(
                    is_feature=True), to_attr='image_feature')
            ).all()),
        ).get(id=id, order_key=request.GET.get('order_key'))

        order_quantity = sum([item.quantity for item in order.items.all()])

        breadcrumb = [
            {"title": _("Order Details")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Order Details")},
        ]

        return render(request, template_name='orders/detail.html',
                      context={'order': order, "breadcrumb": breadcrumb, "order_quantity": order_quantity})
    except Order.DoesNotExist:
        return redirect('main:index')
