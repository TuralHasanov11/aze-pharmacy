from cart.processor import CartProcessor
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET


@require_GET
def summary(request):
    cart = CartProcessor(request)
    breadcrumb = [
        {"title": _("Shopping Cart")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Shopping Cart")},
    ]
    return render(request, 'cart/summary.html', {'cart': cart, "breadcrumb": breadcrumb})


