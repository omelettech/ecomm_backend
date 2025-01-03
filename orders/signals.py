from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from orders.models import Order, Shipping, OrderItem
from payments.models import Payment


@receiver(post_save, sender=Order)
def create_shipping(sender, instance, created, **kwargs):
    """Create a Shipping instance when a new Order is created via rest-auth.
    and connect it with the current order."""
    if created:
        print("Creating Shipping")
        Shipping.objects.create(order=instance)
    instance.save()

# def create_payment(sender, instance, created, **kwargs):
#     """Create a Payment instance when a new Order is created via rest-auth.
#     and connect it with the current order."""
#     if created:
#         print("Creating Payment")
#         Payment.objects.create(
#             order=instance,
#             total_amount=instance.total_price
#         )
#     instance.save()



