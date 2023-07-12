from django.contrib import admin

from django_ecommerce_01.cart.models import (
    Product,
    Order,
    OrderItem,
    ColorVariation,
    SizeVariation,
    Address
    )

class OrderItemAdmin(admin.ModelAdmin):
    list_filter = ['order__user'] 
    list_display = ['pk' ,"order", "quantity", 'product']

class AddressAdmin(admin.ModelAdmin):
    list_display = [
                    'user',
                    'address_line_1',
                    'address_line_2',
                    'city',
                    'zip_code',
                    'default',
                    ]



admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)


