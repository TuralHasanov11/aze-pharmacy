from orders.models import Order


def confirmOrder(order: Order):
    order.payment_status = Order.PaymentStatus.PAID
    order.save()
