from django.contrib import admin
from django.urls import path, include
from orders.views import *

urlpatterns = [
    path('v1/order', OrderListCreateApiView.as_view(), name="order_view"),
    path('v1/order/<int:pk>', OrderRetrieveUpdateDeleteApiView.as_view()),

    path('v1/order_item', OrderItemListCreateApiView.as_view(), name="order_view"),
    path('v1/order_item/<int:order_item_id>', OrderItemRetrieveUpdateDelete.as_view())
]
