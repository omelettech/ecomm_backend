from django.contrib import admin
from django.urls import path, include
from orders.views import *

urlpatterns = [
    path('v1/orders', OrderItemListCreateApiView.as_view(), name="order_view"),
    path('v1/orders/<int:order_id>', OrderRetrieveUpdateDeleteApiView.as_view())
]
