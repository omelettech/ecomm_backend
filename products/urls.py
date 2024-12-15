from django.urls import path, include
from products.views import ProductView

# HOST:PORT/products/v1/
urlpatterns = [
    path('v1/', ProductView.as_view()),
    path('v1/<int:product_id>', ProductView.as_view())

]
