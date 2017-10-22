import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.utils import timezone

from strade import settings


class Image(models.Model):
    filename = models.CharField(max_length=500, default="default")
    file = models.ImageField(upload_to='image')
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.filename


class StoreCategory(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.name


class StoreStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " " + self.name


class Store(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(StoreStatus, on_delete=models.CASCADE, null=True)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True)

    @property
    def image_url(self):
        if self.image is None:
            return None
        return os.path.join(settings.BASE_URL, 'media/image/' + self.image.filename)

    def __str__(self):
        return str(self.id) + " " + self.name


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.ForeignKey(Group, related_name='role', null=True)
    store = models.OneToOneField(Store, on_delete=models.CASCADE, null=True)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def full_name(self):
        return self.get_full_name

    @property
    def image_url(self):
        return os.path.join(settings.BASE_URL, 'media/image/' + self.image.filename)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    store = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.name

    @property
    def image_url(self):
        return os.path.join(settings.BASE_URL, 'media/image/' + self.image.filename)


class RequestStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " " + self.name


class Request(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    address = models.TextField(default="")
    note = models.TextField(default="", null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.buyer) + " -> " + str(self.seller);


class RequestItem(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id) + " " + self.item.name


class UserLocationStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " " + self.name


class UserLocation(models.Model):
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    current_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + " " + self.current_address
