import datetime

from django.db import models


# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to='images/product_images')  # Path to store images on the server
    alt = models.TextField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"+ " | " + self.image.name


class GalleryItem(models.Model):
    # Specifically for gallery page
    image = models.ImageField(upload_to="images/gallery_images/")
    title = models.TextField(max_length=255, default="Untitled")
    description = models.TextField(max_length=450, null=True, blank=True)
    year = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title + " | " + self.image.name
