from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAdminUser

from pictures.models import GalleryItem, Image
from pictures.serializers import GalleryItemSerializer, ImageSerializer


class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def post(self):
        return JsonResponse({"message": "Post not allowed"}, status=405)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]