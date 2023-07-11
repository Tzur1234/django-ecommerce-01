from django.shortcuts import render
from django_ecommerce_01.cart.serializers import ProductSerializer
from django_ecommerce_01.cart.models import Product, OrderItem, ColorVariation, SizeVariation, Order
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django_ecommerce_01.cart.utilize import get_or_set_order
from rest_framework import status


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



"""
The view add a new Item to the cart
if succuss: return the details of the new item
if fail : return a message    
"""
class AddToCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            # Data from the client
            product = Product.objects.get(slug=kwargs['slug'])
            quantity = request.data["quantity"]
            color = ColorVariation.objects.get(id=request.data["color_id"])
            size = SizeVariation.objects.get(id=request.data["size_id"])


            # Create / Retreive Order
            order = get_or_set_order(request)

            # OrderItem 
            order_item = order.items.filter(product=product,
                                            color=color,
                                            size=size,
                                             )
            
            # Update exists OrderItem
            if order_item.exists():
                order_item = order_item.first()
                last_quantity = order_item.quantity
                order_item.quantity = last_quantity + order_item.quantity 
                order_item.save()
            
            # create new OrderItem
            else:
                new_order_item = OrderItem(order=order,
                                           product=product,
                                           size=size,
                                           color=color,
                                           quantity=quantity
                                           )
                new_order_item.save()
            
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

        
        data = {
        'message': f"The item {product.title}, was added to the cart !",
        'alert': 'success'
        }
        return Response(data, status=status.HTTP_200_OK)
    


    

        

        
     

