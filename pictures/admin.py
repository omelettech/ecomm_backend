from django.contrib import admin

# Register your models here.
from pictures.models import *

admin.site.register(Image)
admin.site.register(GalleryItem)