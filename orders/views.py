import random
import string

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from orders.models import Order, OrderItem, Cart, CartItem
from orders.serializers import OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer
from payments.models import Payment
from products.models import ProductSku


def perform_create_order_items(order_instance, cart_items_data):
    for cart_item in cart_items_data:
        print(cart_item['id'])
        product_sku_instance = ProductSku.objects.get(sku=cart_item['product_sku'])
        quantity = cart_item['quantity']
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
        ordernum = generate_order_number()

        total_price = 0
        order_buffer = Order.objects.create(order_number=ordernum, customer=self.request.user.customer)
        order_item_buffer = []

        for cart_item in cart_items_data:
            # make a new cart item object
            product_sku = cart_item.product_sku
            # TODO: Create functions that checks if product sku exists and if quantity is good,
            #  use it for both order and cart
            order_item_buffer.append(
                OrderItem.objects.create(
                    order=order_buffer,
                    product_sku=product_sku,
                    quantity=cart_item.quantity
                )
            )

            total_price += cart_item.product_sku.price * cart_item.quantity
        print(total_price)

        return JsonResponse({"Order created": f"{order_item_buffer[0].order}"})

    # def generate_ordernum(self, serializer):
    #     ordernum = generate_order_number()
    #
    #     # Create A orderitem instance if doesnt exist
    #     # order_items_data = self.request.data.get("order_items", {})
    #     cart_items_data = self.request.user.customer.cart.cartitem_set.all()
    #     print(cart_items_data)
    #
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

    def post(self, request, *args, **kwargs):

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
            cart=self.get_queryset()[0],
            product_sku=product_sku,
            defaults={'quantity': int(quantity)},  # providing quantity only for creation
            deleted_at__isnull=True  # Ensures only non-deleted rows are considered
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.serializer_class(Cart.objects.get(customer=self.request.user.customer))
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class CartItemRetrieveUpdateDestroyApiView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def getCart(self):
        return Cart.objects.filter(customer=self.request.user.customer)

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.getCart)

    def perform_destroy(self, instance):
        instance.soft_delete()

    def destroy(self, request, *args, **kwargs):
        cart = Cart.objects.get(customer=self.request.user.customer)
        id = self.kwargs.get('pk')

        instance = CartItem.objects.get(cart=cart, id=id)
        serializer = self.serializer_class(instance)
        print(instance, serializer)

        if not instance.DoesNotExist:
            return JsonResponse({"error": f"Cart item does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_destroy(instance)
        except AssertionError:
            return JsonResponse({"error": f"Cart item does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError:
            return JsonResponse({"error": f"Cart item does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT, safe=False)
