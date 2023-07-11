from django.contrib import admin

from django_ecommerce_01.cart.models import (
    Product,
    Order,
    OrderItem,
    ColorVariation,
    SizeVariation
    )

class OrderItemAdmin(admin.ModelAdmin):
    list_filter = ['order__user'] 
    list_display = ['pk' ,"order", "quantity", 'product']


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)


