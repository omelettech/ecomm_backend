import random
import string

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from payments.models import Payment
from products.models import ProductSku


def _perform_create_order_items(order_instance, order_items_data):

    for order_item in order_items_data:
        product_sku_instance = ProductSku.objects.get(sku=order_item['product_sku'])
        quantity = order_item['quantity']
        print(product_sku_instance)

        if product_sku_instance is None:
            raise ValueError("Product SKU not found")
        OrderItem.objects.create(order=order_instance,product_sku=product_sku_instance, quantity=quantity)

class OrderListApiView(generics.ListAPIView):
    # LIST
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)

class OrderCreateApiView(generics.CreateAPIView):
    # CREATE AND LIST
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        unique_suffix = ''.join(random.choices(string.digits, k=8))
        ordernum = f"ORD#{unique_suffix}"

        # Create A orderitem instance if doesnt exist
        order_items_data = self.request.data.get("order_items", {})
        if order_items_data:
            order_instance = serializer.save(customer=self.request.user.customer, order_number=ordernum)
            _perform_create_order_items(order_instance, order_items_data)
        else:
            raise ValueError("Order Items are required")


class OrderRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    # GET PUT DELETE
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        order_items_data = self.request.data.get("order_items", [])
        if order_items_data:
            instance = self.get_object()
            instance.orderitem_set.all().delete()
            _perform_create_order_items(instance, order_items_data)
            instance.update_edited_time()
            instance.save()
        else:
            raise ValueError("Order Items are required")
        serializer.save()


    def patch(self, request, *args, **kwargs):
        # Patch will update edited_at

        return JsonResponse({"message": "Patch not allowed"}, status=405)

    def retrieve(self, request, *args, **kwargs):
        if self.get_object().customer != request.user.customer:
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
    permission_classes = [IsAdminUser]

# Create your views here.
