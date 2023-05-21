from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from wishlist.processor import WishlistProcessor


@require_GET
def wishlist(request):
    result = WishlistProcessor(request)
    breadcrumb = [
        {"title": _("Wishlist")},
        {"title": _("Home"), "route": reverse("main:index")},
        {"title": _("Wishlist")},
    ]
    return render(request, 'wishlist/wishlist.html', {
        'wishlist': result,
        'breadcrumb': breadcrumb
    })
