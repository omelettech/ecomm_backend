from django.contrib import admin

# Register your models here.
from users.models import Customer, Wishlist, WishlistItem

admin.site.register(Customer)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)