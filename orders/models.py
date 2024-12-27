from django.core.validators import MinValueValidator
from django.db import models

from products.models import ProductSku
from users.models import Customer


class ShippingAddress(models.Model):
    pass

class Shipping(models.Model):
    #id
    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)




class Order(models.Model):
    ORDER_STATUS = [
        ("Placed", "Placed"),
        ("Failed", "Failed"),
        ("Processing", "Processing"),
        ("Cancelled", "Cancelled"),
        ("Shipping", "Shipping"),
        ("Complete", "Complete"),
    ]
    # id
    order_number = models.CharField(max_length=50,unique=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping=models.ForeignKey(Shipping,on_delete=models.CASCADE)


    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_sku = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.product_sku.product} | ${self.product_sku.price} | ({self.quantity})'

# Create your models here.
