from rest_framework import serializers

from orders.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= "__all__"

