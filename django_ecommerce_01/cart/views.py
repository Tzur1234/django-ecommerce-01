from django.shortcuts import render
from django_ecommerce_01.cart.serializers import ProductSerializer, OrderItemSerializer, AddressSerializer
from django_ecommerce_01.cart.models import Product, OrderItem, ColorVariation, SizeVariation, Order, Address
from django_ecommerce_01.cart.permissions import DeleteOrderItemPermission, IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django_ecommerce_01.cart.utilize import get_or_set_order, check_delete_request, check_update_requst
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


class AddToCartAPIView(APIView):
    """
    The view add a new Item to the cart
    request body : quantity (int), size_id (int), color_id (int)
    response : message (string) , alert (string)
    """
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
            
            if order_item.exists():
                order_item = order_item.first()
                last_quantity = order_item.quantity
                order_item.quantity = last_quantity + order_item.quantity # Update OrderItem quantity
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
    Return all OrderItem relate to the user
    input : No input
    method: GET 
    output: JSON response
    """
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Return all OrderItems that:
        # relate to the the last Open Order
        return OrderItem.objects.filter(
        order_id = self.request.user.order_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # Add extra content to the response
        try:
            order_id = request.user.order_id
            order = Order.objects.get(id=order_id, ordered=False)

            extra_content = {
            'total': f'{order.get_total()}',
            'subtotal': f'{order.get_subtotal()}'
            } 

            # Modify the response data
            response_data = {
                'data': serializer.data,
                'extra_content': extra_content
            }
                
        except Exception as e:
            print('Error in getting extra data: ', e)

        return Response(response_data)


class OrderItemDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def delete(self, request, id):
        
        ## Validation ##
        response_obj = check_delete_request(request, id)
        if response_obj:
            return response_obj

        # Commit delete
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
    Input:  'add' parameter ('True' / 'False') 

    """

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        
        #  Request Validation #
        response_obj = check_update_requst(request, kwargs['id'])
        if response_obj:
            return response_obj

        
        # UPDATE QUANTITY
        order_item = OrderItem.objects.get(id=kwargs['id'])
        add_more_item = request.data.get('add')
        if add_more_item == 'False':
            if order_item.quantity == 1:
                data = {
                'message': " There is only one single Item left !",
                'alert': "warning",
                }
                return Response(data ,status=status.HTTP_403_FORBIDDEN)
            else:                
                data = {
                'message': "One item was removed",
                'alert': "success",
                }
                order_item.quantity = order_item.quantity - 1
                order_item.save()

        else:
            order_item.quantity = order_item.quantity + 1
            order_item.save()

            data = {
                'message': "Item was added !",
                'alert': "success",
            }
        return Response(data ,status=status.HTTP_200_OK)


class AddressUpdateRetrieveAPIView(generics.RetrieveUpdateAPIView):
    """
    The view update the user's address.
    GET : checko if the user has alredy related address object.
    if not : create a new one and attach it to the user.

    PUT: when receiving PUT request it validates the address data.
    if validation was successfuly made, it will return 200 response. Else 400


    permission: the user can update only it's own data.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
      
    def get_object(self):
        # Retrieve a single instance (Address) based on the user field
        try:
            address = Address.objects.get(user=self.request.user)
        except Address.DoesNotExist:
            address = Address.objects.create(user=self.request.user)

        return address

    def get(self, request, *args, **kwargs):
        # Retrieve the instance using get_object() method
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Retrieve the instance using get_object() method
        instance = self.get_object()

        # Validate the address data
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'saved_address_info' : serializer.data,
                'message' : "Your address info was saved",
                'alert' : "success",
            }
            return Response(data, status.HTTP_200_OK)
        else:
            data = {
                'message' : serializer.errors,
                'alert' : "danger",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    


     

