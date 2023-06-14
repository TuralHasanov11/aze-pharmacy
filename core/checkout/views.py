from cart.processor import CartProcessor
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from orders.models import Order
from orders.processor import OrderProcessor


@require_GET
def index(request):
    cart = CartProcessor(request)
    breadcrumb = [
        {"title": _("Checkout")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Checkout")},
    ]
    return render(request, "checkout/index.html", context={
        'cart': cart,
        "breadcrumb": breadcrumb,
    })


@require_GET
def failed(request):
    try:
        orderProcessor = OrderProcessor(request=request)
        order = Order.objects.get(order_id=orderProcessor.order.get("order_id", None),
                                  order_key=orderProcessor.order.get(
                                      "order_key", None),
                                  payment_status=Order.PaymentStatus.FAILED
                                  )
        breadcrumb = [
            {"title": _("Order failed")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Order failed")},
        ]
        return render(request, template_name='checkout/failed.html', context={"breadcrumb": breadcrumb, "order": order})
    except Order.DoesNotExist:
        return redirect("main:index")


@require_GET
def success(request):
    try:
        orderProcessor = OrderProcessor(request=request)
        order = Order.objects.get(order_id=orderProcessor.order.get("order_id", None),
                                  order_key=orderProcessor.order.get(
                                      "order_key", None),
                                  payment_status=Order.PaymentStatus.PAID
                                  )
        breadcrumb = [
            {"title": _("Order succeeded")},
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Order succeeded")},
        ]
        return render(request, template_name='checkout/success.html', context={"breadcrumb": breadcrumb, "order": order})
    except Order.DoesNotExist:
        return redirect("main:index")
