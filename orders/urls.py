from django.contrib import admin
from django.urls import path, include
from orders.views import *

urlpatterns = [
    path('v1/order/', OrderCreateListApiView.as_view(), name="order_view"),
    path('v1/order/withCart', CreateOrderWithCart.as_view(), name="create_order_with_cart"),

    path('v1/order/<int:pk>', OrderRetrieveUpdateDeleteApiView.as_view()),

    path('v1/order_item', OrderItemListCreateApiView.as_view(), name="order_view"),
    path('v1/order_item/<int:pk>', OrderItemRetrieveUpdateDelete.as_view()),

    path('v1/cart/', CartListCreateApiView.as_view(),name="cart_view"),
    path('v1/cart/<int:pk>', CartItemRetrieveUpdateDestroyApiView.as_view())

]
