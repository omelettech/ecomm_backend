from django.core.validators import MinValueValidator
from django.db import models

from products.models import ProductSku


class Order(models.Model):
    # id
    order_number = models.CharField()
    status = models.BooleanField()
    user = models.CharField()  # TODO: change this to use actual users
    # shipping=models.ForeignKey(Shipping)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.product.product} | ${self.unit_price} | ({self.quantity})'

# Create your models here.
