from rest_framework import serializers
from django_ecommerce_01.cart.models import Product, ColorVariation, SizeVariation

class ColorVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariation
        fields = ('id' ,'name',)

class SizeVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariation
        fields = ('id' ,'name',)

class ProductSerializer(serializers.ModelSerializer):
    product_detail_link = serializers.SerializerMethodField(read_only=True)
    add_to_cart_link = serializers.SerializerMethodField(read_only=True)
    color_variation = ColorVariationSerializer(many=True, read_only=True)
    size_variation = SizeVariationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'description',
            'created',
            'updated',
            'active',
            'image',
            'product_detail_link',
            'add_to_cart_link',
            'color_variation',
            'size_variation',
        )

    
    """
     provide the value for the product_detail_link field.
     it uses 'build_absolute_uri' to generate the absolute URL 
     for the product's detail view.
    """
    def get_product_detail_link(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.get_absolute_url())
        return None
    
    def get_add_to_cart_link(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.get_absolute_url_add_to_cart())
        return None