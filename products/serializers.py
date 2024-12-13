from rest_framework import serializers

from products.models import Product, ProductSkus


class ProductSkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSkus
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
