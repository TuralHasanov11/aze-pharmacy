from django.contrib import admin
from orders.models import Order, OrderDelivery, OrderItem
from simple_history.admin import SimpleHistoryAdmin


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderDeliveryInline(admin.StackedInline):
    model = OrderDelivery

@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
  list_display = ("full_name", "total_paid", "phone")
  ordering = ("-created_at", )
  inlines = [
        OrderDeliveryInline,
        OrderItemInline,
  ]
