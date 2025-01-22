from rest_framework import serializers

from pictures.models import Image, GalleryItem


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= GalleryItem

