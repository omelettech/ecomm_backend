import random
import string

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderListCreateApiView(generics.ListCreateAPIView):
    # CREATE AND RETRIEVE
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        unique_suffix = ''.join(random.choices(string.digits, k=8))  # Random 8-digit suffix
        order_id = f"ORD#{unique_suffix}"
        serializer.save(user=self.request.user,
                        order_number=order_id)

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
