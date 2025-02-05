from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pictures.views import GalleryItemViewSet

router = DefaultRouter()
router.register(r'GalleryItem',GalleryItemViewSet)  # This will generate the CRUD endpoints

urlpatterns = [
    path('v1/', include(router.urls)),  # Include the router-generated URLs
]