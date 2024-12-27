from rest_framework import serializers

# class UserSerializer(serializers.HyperLinkedModelSerializer):
from users.models import Customer, Wishlist, WishlistItem


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Customer
        fields = ['user', 'username', 'name', 'email', 'preferred_currency', 'shipping_address', 'created_at']


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['wishlist', 'product_sku', 'added_at', 'deleted_at']


class WishlistSerializer(serializers.ModelSerializer):
    wishlistitem_set = WishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['customer', 'wishlistitem_set']
