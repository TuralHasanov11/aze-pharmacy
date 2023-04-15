from cart.processor import CartProcessor
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from orders.forms import OrderForm


@require_http_methods(['GET', 'POST'])
def index(request):
    cart = CartProcessor(request)

    if request.method == 'POST':
        pass
    
    form = OrderForm()
    return render(request, 'checkout/index.html', context={
        'cart': cart,
        'form': form,
    }) 

