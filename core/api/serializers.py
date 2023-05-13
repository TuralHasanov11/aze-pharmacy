from orders.models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'full_name', 'seen', 'is_flagged', "created_at")
    
