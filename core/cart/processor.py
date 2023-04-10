from decimal import Decimal

from store.models import Product


class CartProcessor:
    def __init__(self, request):
        self.session = request.session
        try:
            # {"1": {price: "12", quantity: "100"}, "2": {price: "12", quantity: "100"}}
            cartContainer = self.session["cart"] 
            products = Product.objects.filter(id__in=[key for key in cartContainer.keys()])
        except Exception:
            self.session["cart"] = {}
            cartContainer = {}

        self.cart = {}
        self.products = []
        if cartContainer:
            for product in products:
                self.cart[str(product.id)] = {
                    'price': str(product.regular_price), 
                    'quantity': next(cartContainer[key]["quantity"] for key in cartContainer.keys() if int(key) == product.id )
                }
            self.products = products
            self.session["cart"] = self.cart
        self.save()


    def __iter__(self):
        cart = self.cart.copy()
        for product in self.products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
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
                self.cart[productId] = {'price': str(product.discount_price), 'quantity': quantity}
            
            self.session["cart"] = self.cart
            self.save()
        except Exception as err:
            raise Exception("Product cannot be added or modified in Shopping cart")


    def update(self, productId: int, quantity: int):
        productId = str(productId)
        try:            
            if productId in self.cart:
                self.cart[productId]['quantity'] = quantity

            self.session["cart"] = self.cart
            self.save()
        except Exception as err:
            raise Exception("Product cannot be added or modified in Shopping cart")


    def delete(self, product: Product) -> None:
        try:
            productId = str(product.id)

            if productId in self.cart:
                del self.cart[productId]
                self.session["cart"] = self.cart
                self.save()
        except:
            raise Exception("Product is not removed from Shopping cart")


    def clear(self) -> None:
        try:
            del self.cart
            self.session["cart"] = {}
            self.save()
        except:
            raise Exception("Shopping cart cannot be cleared")


    def save(self) -> None:
        self.session.modified = True