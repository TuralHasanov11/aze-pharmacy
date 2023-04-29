import json

from api import pagination, serializers
from cart.processor import CartProcessor, WishlistProcessor
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, ProductImage


@require_GET
def summary(request):
    cart = CartProcessor(request)
    return render(request, 'cart/summary.html', {'cart': cart}) 


@require_GET
def cart(request):
    cart = CartProcessor(request) 
    return JsonResponse({"cart": cart.cart, "total_price": cart.get_total_price, "total_quantity": len(cart)})


@require_POST
def cartAdd(request):    
    try:
        cart = CartProcessor(request) 
        data = json.load(request)

        product = Product.objects.select_related('category').prefetch_related(
                    Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
                ).get(id=data['product_id'])
        item = cart.create(product=product, quantity=int(data['product_quantity']))
        
        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price, "item": item})
    except Exception as err:
        return HttpResponseBadRequest(str(err))
        

@require_POST
def cartRemove(request):
    try:
        cart = CartProcessor(request)
        data = json.load(request)
        cart.remove(productId=data["product_id"])

        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price}) 
    except Exception as err:
        return HttpResponseBadRequest(str(err))


@require_POST
def cartUpdate(request):
    try:
        cart = CartProcessor(request)
        data = json.load(request)
        cart.update(productId=int(data['product_id']), quantity=int(data['product_quantity']))
            
        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price}) 
    except Exception as err:
        return HttpResponseBadRequest(err.message) 


@require_GET
def wishlist(request):
    result = WishlistProcessor(request)
    return render(request, 'cart/summary.html', {'wishlist': result}) 


@require_POST
def wishlistAdd(request):    
    try:
        wishlist = WishlistProcessor(request) 
        wishlist.add(productId=int(request.POST.get('product_id')))
        return HttpResponse({"message": _("Product was added to Wishlist")})
    except Exception as err:
        return HttpResponseBadRequest(str(err))
        

@require_POST
def wishlistRemove(request):
    try:
        wishlist = WishlistProcessor(request)
        wishlist.remove(productId=request.POST.get('product_id'))
        return HttpResponse({"message": _("Product was removed from Wishlist")})
    except Exception as err:
        return HttpResponseBadRequest(str(err))
    

