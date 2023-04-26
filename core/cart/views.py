import json

from cart.processor import CartProcessor, WishlistProcessor
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from store.models import Product, ProductImage


@require_GET
def summary(request):
    cart = CartProcessor(request)
    return render(request, 'cart/summary.html', {'cart': cart}) 


@require_POST
def cartAdd(request):    
    try:
        cart = CartProcessor(request) 
        productId = int(request.POST.get('product_id'))
        productQuantity = int(request.POST.get('product_quantity'))

        product = Product.objects.select_related('category').prefetch_related(
                    Prefetch('product_image', queryset=ProductImage.objects.filter(is_feature=True), to_attr='image_feature'),
                ).get(id=productId)
        item = cart.create(product=product, quantity=productQuantity)
        
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

        for productId in data.keys():
            cart.update(productId=productId, quantity=int(data[productId]))
            
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