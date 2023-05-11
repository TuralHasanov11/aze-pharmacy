from django.contrib import admin
from orders.models import Order, OrderDelivery, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderDeliveryInline(admin.StackedInline):
    model = OrderDelivery

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ("full_name", "total_paid", "phone")
  ordering = ("-created_at", )
  inlines = [
        OrderDeliveryInline,
        OrderItemInline,
  ]
