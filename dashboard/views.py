from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from dashboard.permissions import IsArtistUser
from dashboard.serializers import ProductForDashboardSerializer
from orders.models import Order
from orders.serializers import OrderSerializer
from pictures.models import GalleryItem
from pictures.serializers import GalleryItemSerializer
from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.
# TODO: Order management
class OrderCRUD(viewsets.ModelViewSet):

    # permission_classes = [IsArtistUser]
    serializer_class = OrderSerializer

    '''
    Queries orders of specific artist user
    '''
    def get_queryset(self):
        customer = self.request.user.customer
        return Order.objects.filter(customer=customer)

# TODO: Products listing
class ProductCRUD(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductForDashboardSerializer


# TODO: Charts

class GalleryViewSet(viewsets.ModelViewSet):
    # queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

    def get_queryset(self):
        return GalleryItem.objects.filter()