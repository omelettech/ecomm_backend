import random
import string

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from orders.models import Order, OrderItem, Cart, CartItem
from orders.serializers import OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer
from payments.models import Payment
from products.models import ProductSku


def _perform_create_order_items(order_instance, order_items_buffer):
    for order_item in order_items_buffer:
        print("rder_item:", order_item)
        product_sku_instance = ProductSku.objects.get(sku=order_item.product_sku.sku)
        quantity = order_item.quantity
        print("prdocutSku instance", product_sku_instance)

        if quantity <= 0:
            raise ValueError("Quantity should be greater than 0")

        OrderItem.objects.create(order=order_instance, product_sku=product_sku_instance, quantity=quantity)
        _update_product_sku_quantity(product_sku_instance, quantity)


def _update_product_sku_quantity(product_sku_instance, quantity_of_orderitem):
    product_sku_instance.quantity -= quantity_of_orderitem
    product_sku_instance.save()


def _empty_cart(cart):
    cart.cartitem_set.all().update(deleted_at=timezone.now())
    cart.save()


class OrderCreateListApiView(generics.ListCreateAPIView):
    # LIST
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)


class CreateOrderWithCart(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart_instance = self.request.user.customer.cart
        cart_items_data = cart_instance.cartitem_set.filter(deleted_at__isnull=True).all()
        total_price = 0
        order_item_buffer = []
        order_buffer = Order(customer=self.request.user.customer)

        for cart_item in cart_items_data:
            print(cart_item)
            # make a new cart item object
            product_sku_instance = cart_item.product_sku
            if product_sku_instance is None:
                raise ValueError("Product SKU not found")

            if product_sku_instance.quantity <= 0:
                return JsonResponse({"error": f"Product variation has no items left"},
                                    status=HTTP_400_BAD_REQUEST)
            if cart_item.quantity > product_sku_instance.quantity:
                return JsonResponse({"error": f"Product variation only has {product_sku_instance.quantity} items left"},
                                    status=HTTP_400_BAD_REQUEST)

            order_item_buffer.append(
                OrderItem(
                    order=order_buffer,
                    product_sku=product_sku_instance,
                    quantity=cart_item.quantity
                )
            )
            total_price += cart_item.product_sku.price * cart_item.quantity

        print(total_price)
        order_buffer.save()  # since cart_item didnt fail we can be almost certain that order will be created
        try:
            _perform_create_order_items(order_buffer, order_item_buffer)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        _empty_cart(cart_instance)
        return JsonResponse({"Order created": f"{order_item_buffer[0].order}"},
                            status=HTTP_201_CREATED)


#
#
# class OrderCreateApiView(generics.CreateAPIView):
#     # CREATE AND LIST
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         total_price = 0
#         order_item_buffer = [order_item for order_item in request.data.get("order_items", [])]
#         order_buffer = Order(customer=self.request.user.customer)
#         print(order_item_buffer)
#         # for order_item in order_item_buffer:
#         #
#         #
#         #
#         # # total_price += cart_item.product_sku.price * cart_item.quantity
#         # print(total_price)
#
#         return JsonResponse({"Order created": f"{order_item_buffer[0].order}"})
#
#     # def generate_ordernum(self, serializer):
#     #     ordernum = generate_order_number()
#     #
#     #     # Create A orderitem instance if doesnt exist
#     #     # order_items_data = self.request.data.get("order_items", {})
#     #     cart_items_data = self.request.user.customer.cart.cartitem_set.all()
#     #     print(cart_items_data)
#     #
#     #     order_instance = serializer.save(customer=self.request.user.customer, order_number=ordernum)
#     #     perform_create_order_items(order_instance, cart_items_data)


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
            quantity = int(self.request.data.get("quantity"))

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
            defaults={'quantity': quantity},  # providing quantity only for creation
            deleted_at__isnull=True  # Ensures only non-deleted rows are considered
        )

        # checking if cart item quantity + quantity is less than product_sku quantity
        if not created:
            if cart_item.quantity + quantity < product_sku.quantity:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                return JsonResponse({"error": f"Product variation only has {product_sku.quantity} items left"})


        serializer = self.serializer_class(Cart.objects.get(customer=self.request.user.customer))
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class CartItemRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        return Cart.objects.filter(customer=self.request.user.customer)

    def get_object(self):
        cart = self.get_cart()[0]
        id = self.kwargs.get('pk')
        return CartItem.objects.get(cart=cart, id=id, deleted_at__isnull=True)

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.get_cart)

    def perform_destroy(self, instance):
        instance.soft_delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Becomes true when a PATCH request sent

        cart = self.get_cart()
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
