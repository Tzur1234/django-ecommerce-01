from django.shortcuts import render
from django_ecommerce_01.cart.serializers import ProductSerializer
from django_ecommerce_01.cart.models import Product
from rest_framework import generics
from rest_framework import permissions


class ProductListAPIView(generics.ListAPIView):
    """
    Show all product in the list
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (
        permissions.AllowAny,
    )
class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Show all product in the list
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = 'slug'  # Set the lookup field to 'slug'

