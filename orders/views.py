import random
import string

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from payments.models import Payment


class OrderListCreateApiView(generics.ListCreateAPIView):
    # CREATE AND LIST
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.customer)

    def perform_create(self, serializer):
        unique_suffix = ''.join(random.choices(string.digits, k=8))  # Random 8-digit suffix
        ordernum = f"ORD#{unique_suffix}"

        order_instance = serializer.save(user=self.request.user.customer, order_number=ordernum)
        # Create a payment instance
        payment_instance = Payment.objects.create(order=order_instance,
                                                  amount=order_instance.total_price)


class OrderRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    # GET PUT DELETE
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        # Patch will update edited_at
        instance = self.get_object()
        instance.update_edited_time()
        instance.save()
        return JsonResponse({"message": "Order edited_at updated"})

    def retrieve(self, request, *args, **kwargs):
        if self.get_object().user != request.user.customer:
            return JsonResponse({"error": "You are not authorized to view this order"}, status=403)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)


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
