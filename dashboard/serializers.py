from rest_framework import serializers

from products.models import Product, ProductSku
from products.serializers import ProductImageSerializer

class ProductSkuSerializerForDashboard(serializers.ModelSerializer):
    class Meta:
        model=ProductSku
        fields=["id",
                "sku",
                "price",
                "quantity",
                "color_attribute",
                "size_attribute",
                "picture_attribute",
                ]
class ProductForDashboardSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    skus = ProductSkuSerializerForDashboard(many=True,read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        depth = 0