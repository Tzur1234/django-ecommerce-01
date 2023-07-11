from rest_framework import serializers
from django_ecommerce_01.cart.models import Product, ColorVariation, SizeVariation, OrderItem

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
    price = serializers.SerializerMethodField(read_only=True)
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
            'price',

        )


    def get_price(self, obj):
        request = self.context.get('request')
        if request is not None:
            return obj.get_total_price()
        return None 
    
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

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    color = ColorVariationSerializer(read_only=True)
    size = SizeVariationSerializer(read_only=True)
    orderitem_delete_link = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'color',
            'size',
            'orderitem_delete_link',       
            'total_price',
        )

    def get_orderitem_delete_link(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.get_absolute_delete_url())
        return None
    def get_total_price(self, obj):
        request = self.context.get('request')
        if request is not None:
            return obj.get_absolute_price()
        return None
