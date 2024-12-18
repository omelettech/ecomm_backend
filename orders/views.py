from django.shortcuts import render
from rest_framework import generics

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderListCreateApiView(generics.ListCreateAPIView):
    # CREATE AND RETRIEVE
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    # GET PUT DELETE
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

# Order Item views
class OrderItemListCreateApiView(generics.ListCreateAPIView):
    # CREATE AND RETRIEVE
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # CREATE AND RETRIEVE
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# Create your views here.
