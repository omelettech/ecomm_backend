from django.contrib import admin

# Register your models here.
from orders.models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Shipping)
admin.site.register(ShippingAddress)