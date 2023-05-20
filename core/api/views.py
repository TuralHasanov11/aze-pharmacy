import json

from api import pagination, serializers
from checkout.serializers import OrderSerializer
from checkout.utils import getCities
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from orders.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required
@api_view(['GET'])
@permission_required(['orders.view_order', 'orders.change_order'], raise_exception=True)
def orders(request):
    search = request.GET.get('search', None)
    isFlagged = bool(request.GET.get('is_flagged', False))
    selectedOrderByValue = request.GET.get('order_by', '-created_at')

    if search:
        searchQuery = SearchQuery(search)
        searchVector = SearchVector("first_name", "last_name", "email", "address", "city", "phone",
                                    "total_paid", "order_key", "payment_status", "notes",)
        ordersQueryset = Order.objects.annotate(
            search=searchVector, rank=SearchRank(searchVector, searchQuery)
        ).filter(search=searchQuery).order_by("rank", selectedOrderByValue)
    else:
        ordersQueryset = Order.objects.order_by(selectedOrderByValue)

    if isFlagged:
        ordersQueryset = ordersQueryset.filter(is_flagged=isFlagged)

    paginator = pagination.OrderPagination()
    orders = paginator.paginate_queryset(ordersQueryset, request)
    serializer = serializers.OrderSerializer(orders, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def cities(request):
    cities = getCities()
    return Response(data=cities)


@login_required
@api_view(['POST'])
@permission_required(['orders.view_order', 'orders.change_order'], raise_exception=True)
def orderFlag(request, id: int):
    order = Order.objects.get(id=id)
    order.is_flagged = not order.is_flagged
    order.save()
    serializer = serializers.OrderSerializer(order)
    return Response(data=serializer.data)
    


@api_view(['GET'])
def orderValidationMessages(request):
    serializer = OrderSerializer()
    messages: dict = {}
    for field in serializer.fields.keys():
        messages[field] = serializer.fields[field].error_messages
    return Response(data=messages)
