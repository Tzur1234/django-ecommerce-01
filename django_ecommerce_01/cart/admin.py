from django.contrib import admin

from django_ecommerce_01.cart.models import Product, Order, OrderItem


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


