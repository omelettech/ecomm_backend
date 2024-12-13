
from django.urls import path, include
from products.views import ProductView


urlpatterns=[
    path('',ProductView.as_view()),
]