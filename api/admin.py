from django.contrib import admin
from api import models

admin.site.register(models.User)
admin.site.register(models.StoreCategory)
admin.site.register(models.OrderStatus)
admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.Image)
admin.site.register(models.UserLocation)
admin.site.register(models.UserLocationStatus)
admin.site.register(models.OrderItem)
admin.site.register(models.StoreStatus)
admin.site.register(models.Store)
