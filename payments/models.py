from django.core.validators import MinValueValidator
from django.db import models

from orders.models import Order
from users.models import Customer


class Payment(models.Model):
    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Complete", "Complete"),
        ("Failed", "Failed"),
        ("Cancelled", "Cancelled"),
    ]
    CURRENCY_CHOICES = [
        ("CAD", "CAD"), ("USD", "USD"), ("EUR", "EUR"), ("GBP", "GBP"),
    ]
    # id
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    total_amount = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default="Pending")
    currency = models.CharField(max_length=4, default="CAD")

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)


class Transaction(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('affirm', 'Affirm'),
        ('afterpay', 'Afterpay'),
    ]
    # id
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    transaction_id = models.CharField(max_length=50)

# Create your models here.
