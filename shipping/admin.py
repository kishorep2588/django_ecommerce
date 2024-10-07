from django.contrib import admin
from . models import ShippingInfo, ShippingCategories, Order, OrderItem, UserPayment

# Register your models here.
admin.site.register(ShippingInfo)
admin.site.register(ShippingCategories)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserPayment)

