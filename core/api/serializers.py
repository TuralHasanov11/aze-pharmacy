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


class OrderRefundCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=5, min_value=0, decimal_places=2, required=False)
    full_refund = serializers.BooleanField()

    def validate(self, data):
        if data['amount'] + self.context["order"].total_refund > self.context["order"].total_paid:
            raise serializers.ValidationError(
                _("Refund amount is greater than order payment amount"))
        return data


class OrderDeliveryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        fields = ('delivery_status', 'delivery_date', 'courier_name', 'tracking_number')

class OrderRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefund
        fields = ('id', 'order', 'amount', 'created_date')
