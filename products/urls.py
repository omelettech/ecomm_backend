from django.urls import path, include
from products.views import *

# HOST:PORT/products/v1/
urlpatterns = [
    path('v1/products', ProductView.as_view()),
    path('v1/products/<int:product_id>', ProductView.as_view()),

    path('v1/product_skus/',ProductSkuListCreateAPIView.as_view()),
    path("v1/product_skus/<int:id>",ProductSkuUpdateDestroyAPIView.as_view())


]
