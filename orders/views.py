import random
import string

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from orders.models import Order, OrderItem, Cart, CartItem
from orders.serializers import OrderSerializer, OrderItemSerializer, CartSerializer
from payments.models import Payment
from products.models import ProductSku


def perform_create_order_items(order_instance, cart_items_data):
    for order_item in cart_items_data:
        product_sku_instance = ProductSku.objects.get(sku=order_item['product_sku'])
        quantity = order_item['quantity']
        print(product_sku_instance)

        if product_sku_instance is None:
            raise ValueError("Product SKU not found")
        if quantity <= 0:
            raise ValueError("Quantity should be greater than 0")
        elif quantity > product_sku_instance.quantity:
            raise ValueError("Quantity should be less than or equal to available quantity")

        OrderItem.objects.create(order=order_instance, product_sku=product_sku_instance, quantity=quantity)
        update_product_sku_quantity(product_sku_instance, quantity)


def update_product_sku_quantity(product_sku_instance, quantity_of_orderitem):
    product_sku_instance.quantity -= quantity_of_orderitem
    product_sku_instance.save()


class OrderListApiView(generics.ListAPIView):
    # LIST
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)


def generate_order_number():
    unique_suffix = ''.join(random.choices(string.digits, k=8))
    return f"ORD#{unique_suffix}"


class OrderCreateApiView(generics.CreateAPIView):
    # CREATE AND LIST
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart_items_data = self.request.user.customer.cart.cartitem_set.all()
        print(cart_items_data)
        print(cart_items_data)
        if cart_items_data:
            return self.create(request, *args, **kwargs)
        else:
            raise ValueError("cart Items are required")

    # def perform_create(self, serializer):
    #     ordernum = generate_order_number()
    #
    #     # Create A orderitem instance if doesnt exist
    #     # order_items_data = self.request.data.get("order_items", {})
    #     order_instance = serializer.save(customer=self.request.user.customer, order_number=ordernum)
    #     perform_create_order_items(order_instance, cart_items_data)


class OrderRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    # GET PUT DELETE
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def put(self, request, *args, **kwargs):
        # PUT will update edited_at
        # TODO: Implement this
        return JsonResponse({"message": "Put not allowed"}, status=405)

    # def perform_update(self, serializer):
    #     order_items_data = self.request.data.get("order_items", [])
    #     if order_items_data:
    #         instance = self.get_object()
    #         instance.orderitem_set.all().delete()
    #         perform_create_order_items(instance, order_items_data)
    #         instance.update_edited_time()
    #         instance.save()
    #     else:
    #         raise ValueError("Order Items are required")
    #     serializer.save()

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
class CartListCreateApiView(generics.ListCreateAPIView):
    # CREATE AND LIST
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user.customer)

    def post(self, request, *args, **kwargs):  # TODO: implement feature to add cart items to cart

        try:
            product_sku = ProductSku.objects.get(sku=self.request.data.get('product_sku'))
            quantity = self.request.data.get("quantity")

            if not quantity:
                return JsonResponse({"error": f"Quantity not provided"})
            elif quantity > product_sku.quantity:
                return JsonResponse({"error": f"Product variation only has {product_sku.quantity} items left"})

        except ProductSku.DoesNotExist:
            return JsonResponse({"error": "Product Sku does not exist"})


        # Check if cart item already exists, if it does update quantity
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.get_queryset(),
            product_sku=product_sku,
            defaults={'quantity': int(quantity)}  # providing quantity only for creation
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.serializer_class(Cart.objects.get(customer=self.request.user.customer))
        return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
