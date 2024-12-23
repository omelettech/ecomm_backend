from rest_framework import serializers

from products.models import Product, ProductSku, SizeAttribute, ColorAttribute


class ProductSkuSerializer(serializers.ModelSerializer):
    size_attribute_value = serializers.SerializerMethodField()

    class Meta:
        model = ProductSku
        fields = ["product",
                  "sku",
                  "price",
                  "quantity",
                  "created_at",
                  "edited_at",
                  "color_attribute",
                  "size_attribute_value",
                  "size_attribute", ]
    def get_size_attribute_value(self, obj):
        return obj.size_attribute.value if obj.size_attribute else None


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


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
