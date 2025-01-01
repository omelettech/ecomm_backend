from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import Customer


class Product(models.Model):
    # id=auto_gen
    name = models.CharField(max_length=255, null=False, blank=False)  # blank is for forms, null is for database level
    description = models.TextField(blank=True)  # '' blank string for empty form submission
    summary = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=50, blank=False, default="none")

    # cover

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return f"name: {self.name}"


# Different attributes

class ProductAttribute(models.Model):
    # id
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    # override this value in the child classes
    value = models.CharField(blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.value}"


class SizeAttribute(ProductAttribute):
    value = models.CharField(blank=False, max_length=256)


class ColorAttribute(ProductAttribute):
    value = models.CharField(blank=False, max_length=256)


# for every new attribute table add an attr id to ProductSkus table
class ProductSku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField(max_length=55, blank=False, null=False, unique=True)
    price = models.FloatField(default=0, blank=False, null=False)
    quantity = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    # Add attributes here
    color_attribute = models.ForeignKey(ColorAttribute, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    size_attribute = models.ForeignKey(SizeAttribute, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        return f"{self.product} | {self.sku}"



class Review(models.Model):
    # id
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.customer} | {self.rating}"

