from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pictures.views import GalleryItemViewSet, ImageViewSet

router = DefaultRouter()
router.register(r'galleryItem',GalleryItemViewSet)  # This will generate the CRUD endpoints
router.register(r"images",ImageViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),  # Include the router-generated URLs
]
