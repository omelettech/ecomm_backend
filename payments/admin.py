from django.contrib import admin

# Register your models here.
from payments.models import Transaction, Payment

admin.site.register(Payment)
admin.site.register(Transaction)