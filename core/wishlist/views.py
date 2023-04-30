import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
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


@require_POST
def add(request):
    try:
        data = json.load(request)
        wishlist = WishlistProcessor(request)
        wishlist.add(productId=int(data['product_id']))
        return JsonResponse({'quantity': wishlist.__len__()})
    except Exception as err:
        return HttpResponseBadRequest(str(err))


@require_POST
def remove(request):
    try:
        data = json.load(request)
        wishlist = WishlistProcessor(request)
        wishlist.remove(productId=int(data['product_id']))
        return JsonResponse({'quantity': wishlist.__len__()})
    except Exception as err:
        return HttpResponseBadRequest(str(err))
