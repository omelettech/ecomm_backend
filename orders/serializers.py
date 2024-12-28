from rest_framework import serializers

from orders.models import OrderItem, Order, CartItem, Cart


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)

    shipping_set = serializers.StringRelatedField(read_only=True)
    payment_set = serializers.StringRelatedField(read_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields= ["id", "order_number", "status", "user", "created_at", "edited_at",
                 "orderitem_set", "shipping_set", "payment_set","total_price"]

    def get_total_price(self, obj):
        total = 0
        print(obj.orderitem_set.all())
        for item in obj.orderitem_set.all():
            total += item.product_sku.price * item.quantity
        return total



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
