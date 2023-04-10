from cart.processor import CartProcessor
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from store import models


@require_GET
def cart(request):
    cart = CartProcessor(request)
    return render(request, 'cart/summary.html', {'cart': cart}) 


@require_POST
def cartAdd(request):    
    try:
        cart = CartProcessor(request) 
        productId = int(request.POST.get('product_id'))
        productQuantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(models.Product, id=productId)
        cart.create(product=product, quantity=productQuantity)
        
        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price})
    except Exception as err:
        return HttpResponseBadRequest(err.message)
        

@require_POST
def cartDelete(request):
    try:
        cart = CartProcessor(request)
        productId = int(request.POST.get('product_id'))
        cart.delete(product= productId)

        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price}) 
    except Exception as err:
        return HttpResponseBadRequest(err.message)


@require_POST
def cartUpdate(request):
    try:
        cart = CartProcessor(request)
        productId = int(request.POST.get('product_id'))
        productQuantity = int(request.POST.get('product_quantity'))
        cart.update(productId= productId, quantity= productQuantity)

        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price}) 
    except Exception as err:
        return HttpResponseBadRequest(err.message) 
