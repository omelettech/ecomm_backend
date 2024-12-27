from rest_framework import serializers

from orders.models import OrderItem, Order, CartItem, Cart


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= "__all__"

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= "__all__"
        read_only_fields = ['customer', 'order_number', 'created_at', 'status']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields= "__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields= "__all__"
