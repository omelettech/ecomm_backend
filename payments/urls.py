from django.urls import path
from .views import *


urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/<int:pk>/', PaymentView.as_view(), name='payment'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('transaction/<int:pk>/', TransactionView.as_view(), name='transaction'),
    ]