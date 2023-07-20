from django.contrib import admin

from django_ecommerce_01.cart.models import (
    Product,
    Order,
    OrderItem,
    ColorVariation,
    SizeVariation,
    Address,
    Payment,
    )

class OrderItemAdmin(admin.ModelAdmin):
    list_filter = ['order__user', 'order'] 
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

class PaymentAdmin(admin.ModelAdmin):
    list_display = [
                    'order',
                    'payment_method',
                    'timestamp',
                    'successful',
                    'amount',
                    'raw_response',
                    ]
    list_filter = ['order'] 


class OrderAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'ordered']
    list_filter = ['user'] 


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'created',
        'price',
        'active',
    )
    list_editable = ('slug', 'active',)




admin.site.register(Product, ProductAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)


