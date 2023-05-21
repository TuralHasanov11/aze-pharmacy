
from cart.processor import CartProcessor
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET', 'POST'])
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
