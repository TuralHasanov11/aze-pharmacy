from api import pagination, serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from orders.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO: permissions


@login_required
@api_view(['GET'])
@permission_required(['orders.view_order', 'orders.change_order'], raise_exception=True)
def orders(request):
    paginator = pagination.OrderPagination()
    orders = paginator.paginate_queryset(Order.objects.all(), request)
    serializer = serializers.OrderSerializer(orders, many=True)
    return paginator.get_paginated_response(serializer.data) 


@login_required
@api_view(['POST'])
@permission_required(['orders.change_order'], raise_exception=True)
def verifyOrder(request, orderId: int):
    order = get_object_or_404(Order.objects.filter(billing_status=False), id=orderId)
    order.save()
    return Response(data={'message': 'Verified order'})


