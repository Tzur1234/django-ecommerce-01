from django.shortcuts import render
from django_ecommerce_01.cart.serializers import ProductSerializer
from django_ecommerce_01.cart.models import Product, OrderItem
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django_ecommerce_01.cart.utilize import get_or_set_order_session
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
            # Retreive the current active Order
            order = get_or_set_order_session(request)
            product = Product.objects.get(slug=kwargs['slug'])

            # Bring the OrderItem associated with Order and Product
            order_item = order.items.filter(product=product)

            
            if order_item.exists():
                order_item = order_item.first()
                order_item.quantity += 1
                order_item.save()
            
            # create new OrderItem
            else:
                new_order_item = OrderItem(order=order, product=product)
                new_order_item.save()
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

        
        data = {
        'message': f"The item {product.title}, was added to the cart !",
        'alert': 'success'
        }
        return Response(data, status=status.HTTP_200_OK)
    

        

        





        # Retreive the OrderItem ( if exist)


        return Response({"message": f"Authenticated user POST request successful. is Authnticated: {request.user.is_authenticated} "}, status=status.HTTP_200_OK)

