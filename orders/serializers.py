from rest_framework import serializers

from orders.models import OrderItem, Order, CartItem, Cart
from products.serializers import ProductSkuSerializer  # Import the related serializer


class OrderItemSerializer(serializers.ModelSerializer):
    price= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields= ["id","order", "product_sku", "quantity", "price"]

    def get_price(self, obj):
        return obj.product_sku.price

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True,required=False)
    customer = serializers.StringRelatedField(read_only=True)
    shipping_set = serializers.StringRelatedField(read_only=True)
    payment_set = serializers.StringRelatedField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields= ["id", "order_number", "status", "customer", "created_at", "edited_at",
                 "orderitem_set", "shipping_set", "payment_set","total_price"]

    def get_total_price(self, obj):
        total = 0
        for item in obj.orderitem_set.all():
            total += item.product_sku.price * item.quantity
        return total

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= "__all__"
        read_only_fields = ['customer', 'order_number', 'created_at', 'status']


class CartItemSerializer(serializers.ModelSerializer):
    product_sku = serializers.SerializerMethodField()


    class Meta:
        model = CartItem
        fields= "__all__"
        read_only_fields = ['cart','product_sku']

    def get_product_sku(self,obj):
        related_skus = obj.product_sku # Adjust the related name if needed
        return ProductSkuSerializer(related_skus, many=False).data


class CartSerializer(serializers.ModelSerializer):
    cartitem_set = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields= ["id", "customer", "cartitem_set"]

    def get_cartitem_set(self, obj):
        # Filter related items where deleted_at is null
        cart_items = obj.cartitem_set.filter(deleted_at__isnull=True)
        return CartItemSerializer(cart_items, many=True).data
