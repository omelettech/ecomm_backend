from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from orders.models import Order, Shipping


@receiver(post_save, sender=Order)
def create_shipping(sender, instance, created, **kwargs):
    """Create a Shipping instance when a new Order is created via rest-auth.
    and connect it with the current order."""
    if created:
        Shipping.objects.create(order=instance)


    instance.save()