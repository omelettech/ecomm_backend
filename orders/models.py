from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from products.models import ProductSku
from users.models import Customer


class ShippingAddress(models.Model):
    # id
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    added_by = models.ForeignKey(Customer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Shipping(models.Model):
    SHIPPING_STATUS = [
        ("Pending", "Pending"),
        ("Complete", "Complete"),
        ("Failed", "Failed"),
        ("Cancelled", "Cancelled"),
    ]
    # id
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_method = models.CharField(max_length=50),
    shipping_cost = models.IntegerField(validators=[MinValueValidator(0)]),
    shipping_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=SHIPPING_STATUS, default="Pending")
    order = models.OneToOneField('Order', on_delete=models.CASCADE)


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
    order_number = models.CharField(max_length=30, unique=True,editable=False)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="Placed")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def update_edited_time(self):
        self.edited_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.order_number} | {self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_sku = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.product_sku.product} | ${self.product_sku.price} | ({self.quantity})'


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_sku = models.ForeignKey(ProductSku, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)



    def soft_delete(self):
        if not self.deleted_at:
            self.deleted_at = timezone.now()
            self.save()
        else:
            raise AssertionError("Cart item already deleted")

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f'{self.product_sku.product} | ${self.product_sku.price} | ({self.quantity})'
# Create your models here.
