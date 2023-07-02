from django.contrib import admin
from django.utils.html import format_html
from orders.models import Order, OrderDelivery, OrderItem
from simple_history.admin import SimpleHistoryAdmin


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderDeliveryInline(admin.StackedInline):
    model = OrderDelivery


@admin.register(OrderDelivery)
class OrderDeliveryAdmin(SimpleHistoryAdmin):
    list_display = ('order', 'delivery_status', 'delivery_date', 'created_at')
    history_list_display = ["changed_fields", "list_changes"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ""
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)

            for change in delta.changes:
                fields += str("{} - from {} to {}. <br/>".format(change.field,
                              change.old, change.new))
            return format_html(fields)
        return None


@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    list_display = ("full_name", "payment_status", "total_paid", "phone", "created_at")
    ordering = ("-created_at", )
    inlines = [
        OrderDeliveryInline,
        OrderItemInline,
    ]
    readonly_fields = ["seen"]
    history_list_display = ["changed_fields", "list_changes"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ""
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)

            for change in delta.changes:
                fields += str("{} - from {} to {}. <br/>".format(change.field,
                              change.old, change.new))
            return format_html(fields)
        return None
