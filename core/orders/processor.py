from store.models import Product


class OrderProcessor:
    def __init__(self, request):
        self.session = request.session
        order = self.session.get("order", {})

        try:
            self.products = Product.products.list_queryset().filter(id__in=[int(key) for key in order["items"].keys()], in_stock=True)
        except Exception:
            self.products = []

        self.order = order
        if self.order:
            for product in self.products:
                self.order["items"][str(product.id)] = next(self.order["items"][key] for key in self.order["items"].keys() if int(key) == product.id),
            self.session["order"] = self.order
        self.save()

    def create(self, order, orderItems):
        self.order = {
            "first_name": order["first_name"],
            "last_name": order["last_name"],
            "address": order["address"],
            "city": order["city"],
            "phone": order["phone"],
            "email": order["email"],
            "notes": order["notes"],
            "items": {}
        }

        for item in orderItems:
            self.order["items"][str(item["id"])] = item["quantity"]
            
        self.session["order"] = self.order
        self.save()

    def clear(self) -> None:
        del self.order
        self.session["order"] = {}
        self.save()

    def save(self) -> None:
        self.session.modified = True
