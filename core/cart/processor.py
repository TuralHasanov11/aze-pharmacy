from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from store.models import Product, ProductImage


def productSerializer(product: Product):
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "category_slug": product.category.slug,
        "image_feature": product.get_image_feature,
    }


class CartProcessor:
    def __init__(self, request):
        self.session = request.session
        try:
            cartContainer = self.session["cart"]
            products = Product.products.list_queryset().filter(
                id__in=[key for key in cartContainer.keys()], in_stock=True)
        except Exception:
            self.session["cart"] = {}
            cartContainer = {}

        self.cart = {}
        self.products = []
        if cartContainer:
            for product in products:
                self.cart[str(product.id)] = {
                    'price': str(product.discount_price),
                    'quantity': next(cartContainer[key]["quantity"] for key in cartContainer.keys() if int(key) == product.id),
                    'product': productSerializer(product)
                }
            self.products = products
            self.session["cart"] = self.cart
        self.save()

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            item['total_price'] = str(
                Decimal(item['price']) * item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def get_total_price(self) -> Decimal:
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def create(self, product: Product, quantity: int):
        productId = str(product.id)
        
        if productId in self.cart:
            self.cart[productId]["quantity"] += quantity
            self.cart[productId]["price"] = str(product.discount_price)
        else:
            self.cart[productId] = {'price': str(
                product.discount_price), 'quantity': quantity}

        if self.cart[productId]["quantity"] > product.maximum_purchase_units:
            raise ValueError(_("You exceeded maximum purchase limit"))
        elif self.cart[productId]["quantity"] < 1:
            self.cart.pop(productId)
            return None

        self.cart[productId]["product"] = productSerializer(product)

        self.session["cart"] = self.cart
        self.save()
        return self.cart[productId]

    def update(self, productId: int, quantity: int):
        productId = str(productId)
        if productId in self.cart:
            if quantity > 0:
                self.cart[productId]['quantity'] = quantity
                self.cart[productId]['total_price'] = str(
                    Decimal(self.cart[productId]['price']) * quantity)
            else:
                self.cart.pop(productId)
                return None

        self.session["cart"] = self.cart
        self.save()
        return self.cart[productId]

    def remove(self, productId: int) -> None:
        productId = str(productId)
        if productId in self.cart:
            del self.cart[productId]
            self.session["cart"] = self.cart
            self.save()

    def clear(self) -> None:
        del self.cart
        self.session["cart"] = {}
        self.save()

    def save(self) -> None:
        self.session.modified = True
