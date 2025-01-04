from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CustomDeleteManager(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract= True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        self.delete()

    def is_deleted(self):
        """Check if the item is soft-deleted."""
        return self.deleted_at is not None


class Customer(CustomDeleteManager):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200)
    preferred_currency = models.CharField(max_length=3, null=True)
    shipping_address = models.ForeignKey("orders.ShippingAddress", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__()

class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.user.username

class WishlistItem(CustomDeleteManager):
    #id
    wishlist = models.ForeignKey("Wishlist", on_delete=models.CASCADE)
    product_sku = models.ForeignKey("products.ProductSku", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return f'{self.wishlist.__str__()} | {self.product_sku.product.name}'


# Create your models here.
