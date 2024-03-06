from django.contrib import admin
from .models import ProductBag,BagItem,Order,PickupPoint,DeliveryMethod
# Register your models here.
admin.site.register(ProductBag)
admin.site.register(Order)
admin.site.register(DeliveryMethod)
admin.site.register(PickupPoint)
admin.site.register(BagItem)