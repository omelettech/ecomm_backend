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

@receiver(post_save, sender=Order)
def update_stock_on_order(sender, instance, created, **kwargs):
    """
    Deduct product_sku quantity when an order is placed.
    This runs only when a new order is created.
    """
    if created:  # Only trigger when a new order is created
        for order_item in instance.orderitem_set.all():  # Fetch related items
            product_sku = order_item.product_sku
            if order_item.quantity > product_sku.quantity:
                instance.status = "Failed"
                instance.save()
                raise ValueError(f"Not enough stock for {product_sku}. Only {product_sku.quantity} left.")
            product_sku.quantity -= order_item.quantity
            product_sku.save()


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



