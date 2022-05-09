from rest_framework import serializers
from .models import Cart, CartItem

class GetAllCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields=('id', 'user', 'create_at', 'updated_at', 'totalPrice', 'is_ordered')

class GetAllCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields=('id', 'cart', 'item', 'price', 'quantity', 'totalPrice')