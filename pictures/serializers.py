from rest_framework import serializers

from ecomm_backend.settings import MEDIA_URL, DOMAIN_URL
from pictures.models import Image, GalleryItem


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class GalleryItemSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(source='image.width', read_only=True)
    height = serializers.IntegerField(source='image.height', read_only=True)
    src = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= GalleryItem
        fields = ['title','description','year','width','height','src']

    '''
    Returns the link of the image only'''
    def get_src(self,obj):
        if obj.image:
            return "http://"+DOMAIN_URL+MEDIA_URL+obj.image.name
        return None
