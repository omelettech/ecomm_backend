from django.contrib import admin

# Register your models here.
from products.models import *

admin.site.register(Product)
admin.site.register(SizeAttribute)
admin.site.register(ColorAttribute)
admin.site.register(ProductSku)
