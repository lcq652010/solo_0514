from django.contrib import admin
from .models import Shop, Product, Rider, Order, OrderItem, DeliveryTracking


admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Rider)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryTracking)
