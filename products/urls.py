from django.urls import path, include
from products.views import *

# HOST:PORT/products/v1/
urlpatterns = [
    path('v1/products/', ProductView.as_view(),name="product_view"),
    path('v1/products/<int:product_id>', ProductView.as_view(),name="product_view"),
    path('v1/products/with_default/',get_products_with_default_variations,name="product_default_function"),
    path('v1/products/featured/',get_featured_products,name="product_featured_function"),

    path('v1/product_skus/',ProductSkuListCreateAPIView.as_view()),
    path("v1/product_skus/<int:id>",ProductSkuUpdateDestroyAPIView.as_view()),
    path("v1/product_skus/search_product/<int:product_id>",ProductSkusByProductId.as_view()),

    path('v1/product_attribute/<str:attribute_name>', ProductAttributeListCreateAPIView.as_view()),
    path("v1/product_attribute/<int:id>", ProductSkuUpdateDestroyAPIView.as_view())

]
