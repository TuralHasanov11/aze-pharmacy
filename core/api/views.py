import json
import logging

from administration.forms import OrderDeliveryForm
from administration.notifications import (sendDeliveryStatusNotification,
                                          sendRefundNotification)
from administration.serializers import OrderDeliveryLogSerializer
from api.serializers import (OrderDeliverySerializer,
                             OrderRefundCreateSerializer,
                             OrderRefundSerializer, OrderSerializer)
from cart.processor import CartProcessor
from checkout.payment import PaymentGateway
from checkout.serializers import CheckoutSerializer
from checkout.utils import getCities
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Prefetch
from django.http import (HttpResponseBadRequest, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from orders.confirm import confirmOrder
from orders.models import Order, OrderDelivery, OrderItem, OrderRefund
from orders.notifications import OrderCreatedEvent
from orders.processor import OrderProcessor
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product, ProductImage
from wishlist.processor import WishlistProcessor

logger = logging.getLogger('main')


@api_view(['GET'])
def cities(request):
    cities = getCities()
    return Response(data=cities)


@login_required
@api_view(['POST'])
@permission_required(['orders.view_order', 'orders.change_order'], raise_exception=True)
def orderFlag(request, id: int):
    try:
        order = Order.objects.get(id=id)
        order.is_flagged = not order.is_flagged
        order.save()
        serializer = OrderSerializer(order)
        return Response(data=serializer.data)
    except Order.DoesNotExist:
        return HttpResponseNotFound(_("Order not found"))
    except Exception as err:
        logger.error(str(err))
        return HttpResponseBadRequest(str(err))


@api_view(['GET'])
def checkoutFormDetails(request):
    lang = request.GET.get('lang', 'az')
    translation.activate(lang)
    try:
        serializer = CheckoutSerializer()
        messages: dict = {}
        for field in serializer.fields.keys():
            messages[field] = {"error_messages": serializer.fields[field].error_messages,
                               "label": serializer.fields[field].label}
        return Response(data=messages)
    except Exception as err:
        logger.error(str(err))
        return HttpResponseBadRequest(str(err))


@require_POST
def wishlistAdd(request):
    try:
        data = json.load(request)
        wishlist = WishlistProcessor(request)
        wishlist.add(productId=int(data['product_id']))
        return JsonResponse({'quantity': wishlist.__len__()})
    except Exception as err:
        return HttpResponseBadRequest(str(err))


@require_POST
def wishlistRemove(request):
    try:
        data = json.load(request)
        wishlist = WishlistProcessor(request)
        wishlist.remove(productId=int(data['product_id']))
        return JsonResponse({'quantity': wishlist.__len__()})
    except Exception as err:
        return HttpResponseBadRequest(str(err))


@require_POST
def cartAdd(request):
    try:
        cart = CartProcessor(request)
        data = json.load(request)

        product = Product.objects.select_related('category').prefetch_related(
            Prefetch('product_image', queryset=ProductImage.objects.filter(
                is_feature=True), to_attr='image_feature'),
        ).get(id=data['product_id'], in_stock=True)

        item = cart.create(product=product, quantity=int(
            data['product_quantity']))

        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price, "item": item})
    except Product.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND,
                            data={"message": _("Product was not found")})
    except Exception as err:
        logger.error(str(err))
        return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={"message": str(err)})


@require_POST
def cartRemove(request):
    try:
        cart = CartProcessor(request)
        data = json.load(request)
        cart.remove(productId=data["product_id"])
        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price})
    except Exception as err:
        return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={"message": str(err)})


@require_POST
def cartUpdate(request):
    try:
        cart = CartProcessor(request)
        data = json.load(request)
        item = cart.update(productId=int(data['product_id']),
                           quantity=int(data['product_quantity']))
        return JsonResponse({'quantity': cart.__len__(), 'total_price': cart.get_total_price, "item": item})
    except Exception as err:
        return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={"message": str(err)})


@require_POST
def checkout(request):
    try:
        cart = CartProcessor(request)
        serializer = CheckoutSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                order = Order(**serializer.validated_data)
                order.total_paid = cart.get_total_price
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order_id=order.id,
                        product_id=item['product']['id'],
                        price=item['price'],
                        sub_total=item['total_price'],
                        quantity=item['quantity']
                    )
                paymentData = PaymentGateway.charge(request=request, description=f"{order.full_name}-{order.total_paid}",
                                                    amount=float(order.total_paid))
                order.order_id = paymentData["payload"]["orderId"]
                order.order_key = paymentData["payload"]["sessionId"]
                order.save()
                orderProcessor = OrderProcessor(request=request)
                orderProcessor.create(
                    orderId=order.order_id, orderKey=order.order_key)
                return JsonResponse(data=paymentData["payload"])
    except Exception as e:
        logger.error(str(e))
        return JsonResponse(status=400, data={"message": _("Order cannot be placed"), "errors": str(e)})


@api_view(['GET', 'POST'])
def approvePayment(request):
    try:
        if request.method == 'POST':
            data = json.load(request)["payload"]
            orderProcessor = OrderProcessor(request=request)
            order = Order.objects.select_related('order_delivery').prefetch_related(
                Prefetch('items', queryset=OrderItem.objects.select_related(
                    'product__category').all()),
            ).get(order_key=data["sessionId"], order_id=data["orderID"],
                  payment_status=Order.PaymentStatus.PENDING)

            confirmOrder(order)

            delivery, created = OrderDelivery.objects.get_or_create(
                order=order)
            sendDeliveryStatusNotification(
                request=request, order=order, delivery=delivery)

            translation.activate("az")
            OrderCreatedEvent(order).dispatch()

            return JsonResponse(data)
        else:
            try:
                orderProcessor = OrderProcessor(request=request)
                order = Order.objects.get(order_id=orderProcessor.order.get("order_id", None),
                                          order_key=orderProcessor.order.get("order_key", None))

                isOrderPaid = PaymentGateway.isPaid(
                    request=request, orderId=order.order_id, orderKey=order.order_key)

                if isOrderPaid and order.payment_status == Order.PaymentStatus.PENDING:
                    confirmOrder(order)
                elif not isOrderPaid:
                    raise Exception(_('Order is pending'))

                cart = CartProcessor(request)
                cart.clear()

                translation.activate("az")
                messages.success(request, _('Order was placed successfully'))
                return redirect('checkout:success')
            except Exception as e:
                logger.error(str(e))
                messages.error(request, _("Order cannot be placed"))
                return redirect(f"{reverse('checkout:failed')}#order-failed")
    except Exception as e:
        logger.error(str(e))
        messages.error(request, _("Order cannot be placed"))
        return JsonResponse(status=400, data={"message": _("Order cannot be placed"), "errors": str(e)})


@api_view(['GET', 'POST'])
def cancelPayment(request):
    try:
        if request.method == 'POST':
            data = json.load(request)["payload"]
            Order.objects.get(
                order_key=data["sessionId"], order_id=data["orderID"]).delete()
            return JsonResponse(data)
        else:
            orderProcessor = OrderProcessor(request=request)
            orderProcessor.clear()
            translation.activate("az")
            return redirect("checkout:index")
    except Exception as e:
        logger.error(str(e))
        return JsonResponse(status=400, data={"message": _("Order cannot be cancelled"), "errors": str(e)})


@api_view(['GET', 'POST'])
def declinePayment(request):
    try:
        if request.method == 'POST':
            data = json.load(request)["payload"]
            order = Order.objects.get(
                order_key=data["sessionId"], order_id=data["orderID"])
            order.payment_status = order.PaymentStatus.FAILED
            order.save()
            return JsonResponse(data)
        else:
            translation.activate("az")
            messages.error(request, _('Your order has failed!'))
            return redirect(f"{reverse('checkout:failed')}#order-failed")
    except Exception as e:
        logger.error(str(e))
        return JsonResponse(status=400, data={"errors": str(e)})


@login_required
@api_view(['POST'])
@permission_required(['orders.change_order'], raise_exception=True)
def orderRefund(request, id: int):
    try:
        order = Order.objects.get(id=id)
        serializer = OrderRefundCreateSerializer(
            data=request.POST, context={"order": order})
        if serializer.is_valid():
            with transaction.atomic():
                data = serializer.validated_data
                if "full_refund" in data and data.get("full_refund"):
                    data["amount"] = order.total_paid

                PaymentGateway.refund(request=request, amount=float(data["amount"]),
                                      orderId=order.order_id, orderKey=order.order_key)
                orderRefund = OrderRefund.objects.create(
                    order=order, amount=data["amount"], reason=data["reason"], created_by=request.user)
                order.payment_status = Order.PaymentStatus.REFUNDED
                order.total_refund += orderRefund.amount
                order.save()

                sendRefundNotification(
                    request=request, order=order, refund=orderRefund)

                orderRefundSerializer = OrderRefundSerializer(
                    instance=orderRefund)
                orderSerializer = OrderSerializer(instance=order)
                return Response(data={"message": _("Order was refunded"),
                                      "order": orderSerializer.data,
                                      "order_refund": orderRefundSerializer.data})
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data={"message": _("Order cannot be refunded"), "errors": serializer.errors})
    except Order.DoesNotExist as e:
        logger.error(str(e))
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": _("Order was not found")})
    except Exception as e:
        logger.error(str(e))
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": _("Refund failed")})


@login_required
@api_view(['POST'])
@permission_required(['orders.change_order'], raise_exception=True)
def updateOrderDelivery(request, id: int):
    try:
        delivery = OrderDelivery.objects.get(order_id=id)
        order = Order.objects.get(id=id)
        form = OrderDeliveryForm(data=request.POST, instance=delivery)
        if form.is_valid():
            context = {}
            if form.has_changed():
                with transaction.atomic():
                    changedData = form.changed_data
                    instance = form.save()
                    logsSerializer = OrderDeliveryLogSerializer(instance=instance,
                                                                logs=instance.history.order_by('-history_date'))
                    latestLog = logsSerializer.save()
                    context["delivery_log"] = latestLog
                    if "delivery_status" in changedData:
                        try:
                            sendDeliveryStatusNotification(
                                request=request, order=order, delivery=delivery)
                        except Exception as e:
                            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": str(e)})
            serializer = OrderDeliverySerializer(instance=delivery)
            context["delivery"] = serializer.data
            context["message"] = _("Order delivery was updated")
            return Response(data=context)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data={"message": _("Order delivery cannot be updated"), "errors": form.errors})
    except Order.DoesNotExist as e:
        logger.error(str(e))
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": _("Order was not found")})
