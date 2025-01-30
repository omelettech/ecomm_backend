from rest_framework import serializers

from pictures.models import Image
from products.models import Product, ProductSku, SizeAttribute, ColorAttribute


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'alt']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

class ProductForCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["name",'description','summary']
# TODO reduce the payload for product serializers

class ProductSkuSerializer(serializers.ModelSerializer):
    size_attribute_value = serializers.SerializerMethodField()
    associated_image = serializers.SerializerMethodField()
    product = ProductForCartSerializer(many=False, read_only=True )

    class Meta:
        model = ProductSku
        fields = ["id",
                  "product",
                  "sku",
                  "price",
                  "quantity",
                  "created_at",
                  "edited_at",
                  "color_attribute",
                  "size_attribute_value",
                  "size_attribute",
                  "picture_attribute",
                  "associated_image"
                  ]

    def get_size_attribute_value(self, obj):
        return obj.size_attribute.value if obj.size_attribute else None

    def get_associated_image(self, obj):
        if obj.picture_attribute and obj.picture_attribute.value:
            # Serialize the `picture_attribute.value` using `ProductImageSerializer`
            return ProductImageSerializer(obj.picture_attribute.value).data
        return None


# noinspection PyPep8
'''
 ______  ______  ______  _____   __  __  ______  ______     ______  ______  ______  ______  __  ______  __  __  ______  ______  ______    
/\  == \/\  == \/\  __ \/\  __-./\ \/\ \/\  ___\/\__  _\   /\  __ \/\__  _\/\__  _\/\  == \/\ \/\  == \/\ \/\ \/\__  _\/\  ___\/\  ___\   
\ \  _-/\ \  __<\ \ \/\ \ \ \/\ \ \ \_\ \ \ \___\/_/\ \/   \ \  __ \/_/\ \/\/_/\ \/\ \  __<\ \ \ \  __<\ \ \_\ \/_/\ \/\ \  __\\ \___  \  
 \ \_\   \ \_\ \_\ \_____\ \____-\ \_____\ \_____\ \ \_\    \ \_\ \_\ \ \_\   \ \_\ \ \_\ \_\ \_\ \_____\ \_____\ \ \_\ \ \_____\/\_____\ 
  \/_/    \/_/ /_/\/_____/\/____/ \/_____/\/_____/  \/_/     \/_/\/_/  \/_/    \/_/  \/_/ /_/\/_/\/_____/\/_____/  \/_/  \/_____/\/_____/ 
'''


class SizeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeAttribute
        fields = '__all__'


class ColorAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorAttribute
        fields = '__all__'
