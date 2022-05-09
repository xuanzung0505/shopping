from rest_framework import serializers
from .models import Order

class GetAllOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=('id', 'user', 'cart', 'shipping_address', 'order_description', 'order_total', 
        'is_completed')