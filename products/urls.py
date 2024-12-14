
from django.urls import path, include
from products.views import ProductView

# HOST:PORT/products/v1/
urlpatterns=[
    path('',ProductView.as_view()),
]