from django.shortcuts import render
from django_ecommerce_01.cart.serializers import ProductSerializer, OrderItemSerializer
from django_ecommerce_01.cart.models import Product, OrderItem, ColorVariation, SizeVariation, Order
from django_ecommerce_01.cart.permissions import DeleteOrderItemPermission
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
request body : quantity (int), size_id (int), color_id (int)
response : message (string) , alert (string)
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
    

class CartAPIView(generics.ListAPIView):
    """
    Show all OrderItem for the last order
    """
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Return all OrderItems that:
        # points to the same open order
        # that are stil open
        return OrderItem.objects.filter(
            order_id = self.request.user.order_id)

  
class OrderItemDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def delete(self, request, id):
        ## Validation ##

        # Check if the OrderItem exists
        obj = OrderItem.objects.filter(id=id)
        if not obj.exists():
            data = {
                'message': "The OrderItem you ask to delete doesn't exists",
                'alert': "warning",
            }
            return Response(data ,status=status.HTTP_404_NOT_FOUND)
        
        # check if the user allowed to delete this OrderIten istance
        if request.user != obj.first().order.user :
            data = {
                'message': "You are not allowed to commit those changes !",
                'alert': "danger",
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        
        order_item = OrderItem.objects.get(id=id)
        order_item.delete()
        data = {
            'message': "Item was removed !",
            'alert': "success",
        }
        return Response(data ,status=status.HTTP_204_NO_CONTENT)


class UpdateOrderItemAPIView(generics.UpdateAPIView):
    """
    API view that only accepts PUT requests to update an OrderItem.
    Receieve in the body 'add' parameter that indicates whether the View show add +1 to the OrderItem 
    or -1
    """

    permission_classes = (permissions.IsAuthenticated,)


    def put(self, request, *args, **kwargs):
        #  Validation #

        # Check if the OrderItem exists
        obj = OrderItem.objects.filter(id=kwargs['id'])
        if not obj.exists():
            data = {
                'message': "The OrderItem doesn't exists",
                'alert': "warning",
            }
            return Response(data ,status=status.HTTP_404_NOT_FOUND)
        
        # check if the user allowed to delete this OrderIten istance
        if request.user != obj.first().order.user :
            data = {
                'message': "You are not allowed to commit those changes !",
                'alert': "danger",
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        
        # UPDATE QUANTITY
        order_item = OrderItem.objects.get(id=kwargs['id'])
        add_more_item = request.data.get('add')
        if add_more_item == 'False':
            print('False !!!')
            if order_item.quantity == 1:
                data = {
                'message': " There is only one single Item left !",
                'alert': "warning",
                }
            else:                
                data = {
                'message': "One item was removed",
                'alert': "success",
                }
                order_item.quantity = order_item.quantity - 1
                order_item.save()

        else:
            print('True !!')
            order_item.quantity = order_item.quantity + 1
            order_item.save()

            data = {
                'message': "Item was added !",
                'alert': "success",
            }
        return Response(data ,status=status.HTTP_200_OK)
        
        
     

