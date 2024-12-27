from rest_framework import serializers

# class UserSerializer(serializers.HyperLinkedModelSerializer):
from users.models import Customer, Wishlist, WishlistItem


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    email = serializers.CharField(source='user.email',read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'username', 'email', 'name', 'preferred_currency', 'shipping_address', 'created_at']


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'wishlist', 'product_sku', 'added_at', 'deleted_at']


class WishlistSerializer(serializers.ModelSerializer):
    wishlistitem_set = WishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'customer', 'wishlistitem_set']
