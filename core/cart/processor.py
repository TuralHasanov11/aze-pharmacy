from decimal import Decimal

from store.models import Product


def productSerializer(product: Product):
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "category_slug": product.category.slug,
        "image_feature": product.image_feature[0].image.url,
    }


class CartProcessor:
    def __init__(self, request):
        self.session = request.session
        try:
            cartContainer = self.session["cart"]
            products = Product.products.list_queryset().filter(id__in=[key for key in cartContainer.keys()])
        except Exception:
            self.session["cart"] = {}
            cartContainer = {}

        self.cart = {}
        self.products = []
        if cartContainer:
            for product in products:
                self.cart[str(product.id)] = {
                    'price': str(product.regular_price),
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
        try:
            if productId in self.cart:
                self.cart[productId]["price"] = str(product.discount_price)
                self.cart[productId]["quantity"] += quantity
            else:
                self.cart[productId] = {'price': str(
                    product.discount_price), 'quantity': quantity}

            self.cart[productId]["product"] = productSerializer(product)

            self.session["cart"] = self.cart
            self.save()
            return self.cart[productId]
        except Exception:
            raise Exception(
                "Product cannot be added or modified in Shopping cart")

    def update(self, productId: int, quantity: int):
        productId = str(productId)
        try:
            if productId in self.cart:
                if quantity > 0:    
                    self.cart[productId]['quantity'] = quantity
                    self.cart[productId]['total_price'] = str(Decimal(self.cart[productId]['price']) * quantity)
                else:
                    self.cart.pop(productId)
                    return None

            self.session["cart"] = self.cart
            self.save()
            return self.cart[productId]
        except Exception:
            raise Exception(
                "Product cannot be added or modified in Shopping cart")

    def remove(self, productId: int) -> None:
        try:
            productId = str(productId)
            if productId in self.cart:
                del self.cart[productId]
                self.session["cart"] = self.cart
                self.save()
        except Exception:
            raise Exception("Product is not removed from Shopping cart")

    def clear(self) -> None:
        try:
            del self.cart
            self.session["cart"] = {}
            self.save()
        except Exception:
            raise Exception("Shopping cart cannot be cleared")

    def save(self) -> None:
        self.session.modified = True

