from django.contrib import admin
from api import models

admin.site.register(models.User)
admin.site.register(models.StoreCategory)
admin.site.register(models.RequestStatus)
admin.site.register(models.Request)
admin.site.register(models.Product)
admin.site.register(models.Image)
