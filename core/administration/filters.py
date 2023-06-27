
from enum import Enum

from django.db.models import Q
from django.db.models.query import QuerySet


class ProductFilterQuery:
    queryset: QuerySet

    def __init__(self, queryset: QuerySet, queryData: dict) -> None:
        self.queryset = queryset
        for field in queryData:
            if queryData[field]:
                self.queryset = self.queryset.filter(**{field: queryData[field]})


class OrderPaymentStatusFilterQuery:
    class Values(Enum):
        PENDING: str = "PENDING"
        PAID: str = "PAID"
        FAILED: str = "FAILED"
        REFUNDED: str = "REFUNDED"

    queryset: QuerySet

    def __init__(self, queryset, status: str = None) -> None:
        self.queryset = queryset
        if status is not None and status.upper() in self.values:
            self.queryset = self.queryset.filter(payment_status=status.upper())

    @property
    def values(self):
        return [item.value for item in self.Values]


class OrderFlaggedFilterQuery:
    queryset: QuerySet

    def __init__(self, queryset, value=False) -> None:
        self.queryset = queryset
        if value:
            self.queryset = self.queryset.filter(is_flagged=True)


class OrderSearchFilterQuery:
    queryset: QuerySet

    def __init__(self, queryset, value: str) -> None:
        self.queryset = queryset
        if value:
            self.queryset = self.queryset.filter(Q(id__icontains=value) | Q(first_name__icontains=value) |
                                                 Q(last_name__icontains=value) | Q(email__icontains=value) |
                                                 Q(address__icontains=value) | Q(city__icontains=value) |
                                                 Q(phone__icontains=value) | Q(total_paid__icontains=value) |
                                                 Q(order_id__icontains=value) | Q(notes__icontains=value))