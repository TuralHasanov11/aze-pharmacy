from cart.processor import CartProcessor


def cart(request):
    return {"cart": CartProcessor(request)}