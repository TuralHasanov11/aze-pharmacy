from django.utils.translation import gettext_lazy as _
from orders.models import Order, OrderDelivery, OrderRefund
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'city', 
                  'phone', 'total_paid', 'total_refund', 'order_key', 'session_id', 
                  'payment_status', 'notes', 'is_flagged', 'seen', 'created_at', 'updated_at', 
                  'get_payment_status_display')


class OrderRefundCreateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=5, min_value=0, decimal_places=2, required=False)
    full_refund = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = OrderRefund
        fields = ('amount', 'full_refund', 'reason')

    def validate_amount(self, value):
        if value + self.context["order"].total_refund > self.context["order"].total_paid:
            raise serializers.ValidationError(
                _("Refund Amount should not be greater than remainder of total payment"))
        return value


class OrderDeliveryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        fields = ('delivery_status', 'delivery_date', 'courier_name', 'tracking_number')

class OrderRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefund
        fields = ('id', 'order', 'reason', 'amount', 'created_date')
