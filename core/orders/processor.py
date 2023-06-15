class OrderProcessor:
    def __init__(self, request):
        self.session = request.session
        self.order = self.session.get("order", {})

    @property
    def orderId(self):
        return int(self.order.get("order_id", 0))
    
    @property
    def orderKey(self):
        return self.order.get("order_key", "")

    def create(self, orderId, orderKey):
        self.order = {
            "order_id": orderId,
            "order_key": orderKey,
        }            
        self.session["order"] = self.order
        self.save()

    def clear(self) -> None:
        del self.order
        self.session["order"] = {}
        self.save()

    def save(self) -> None:
        self.session.modified = True
