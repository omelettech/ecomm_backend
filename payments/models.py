from django.core.validators import MinValueValidator
from django.db import models

from orders.models import Order


class Payment(models.Model):
    #id
    order=models.ForeignKey(Order,on_delete=models.CASCADE,unique=True)
    total_amount=models.IntegerField(null=False,blank=False,validators=[MinValueValidator(0)])
    status=models.CharField(max_length=50,choices=
    [("Pending","Pending"),
     ("Complete","Complete")],default="Pending")
    created_at=models.DateTimeField(auto_now_add=True)
    edited_at=models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(blank=True,null=True,default=None)
    currency=models.CharField(max_length=4,default="CAD")

class Transaction(models.Model):
    #id
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method=models.CharField(max_length=50,choices=
    [("Credit Card","Credit Card"),
     ("Debit Card","Debit Card"),
     ("Paypal","Paypal")])

# Create your models here.

