from cart.processor import CartProcessor
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET


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
def declined(request):
    template_name = 'checkout/declined.html'
    breadcrumb = [
        {"title": _("Order Declined")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Order Declined")},
    ]                
    messages.warning(request, _('Order was declined'))
    return render(request, template_name=template_name, context={"breadcrumb": breadcrumb})