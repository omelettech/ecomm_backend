from django.db import models
from django.contrib.auth.models import User

from orders.models import ShippingAddress

class PaymentMethod(models.Model):
    pass


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200)
    preferred_currency = models.CharField(max_length=3, null=True)
    preferred_payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Create your models here.
