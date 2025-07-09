# dashboard/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dashboard.views import OrderCRUD, ProductCRUD

router = DefaultRouter()
# router.register(r'', ArtistDashboardViewSet, basename='dashboard')
router.register(r"orders",OrderCRUD, basename="OrderManagement")
router.register(r"v1/products",ProductCRUD, basename="ProductManagement")


urlpatterns = [
    path('', include(router.urls)),
]
