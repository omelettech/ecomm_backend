from django.core.validators import MinValueValidator
from django.db import models

from products.models import ProductSku



class ShippingAddress(models.Model):
    pass

class Shipping(models.Model):
    #id
    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)




class Order(models.Model):
    ORDER_STATUS = [
        ("Pending", "Pending"),
        ("Complete", "Complete")
    ]
    # id
    order_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=ORDER_STATUS)
    user = models.CharField(max_length=50)  # TODO: change this to use actual users
    # shipping=models.ForeignKey(Shipping)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_sku = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.product_sku.product} | ${self.product_sku.price} | ({self.quantity})'

# Create your models here.
