from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.utils import timezone


class StoreCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.name


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.ForeignKey(Group, related_name='role', null=True)
    store_name = models.CharField(max_length=50, null=True)
    store_category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def full_name(self):
        return self.get_full_name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField
    store = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.name


class RequestStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " " + self.name


class Request(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.buyer) + " -> " + str(self.seller);
