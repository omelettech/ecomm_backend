from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from orders.models import Cart
from .models import Customer, Wishlist


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    """Create a Customer instance when a new User is created via rest-auth."""
    if created:
        Customer.objects.create(user=instance)
        print(instance)
        print(instance.customer)
        Cart.objects.create(customer=instance.customer)
        Wishlist.objects.create(customer=instance.customer)
    instance.customer.save()

