from django.contrib import admin

from django_ecommerce_01.cart.models import (
    Product,
    Order,
    OrderItem,
    ColorVariation,
    SizeVariation
    )


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)


