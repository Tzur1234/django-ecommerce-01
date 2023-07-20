from django_ecommerce_01.cart.models import (Order,
                                             Address,
                                             OrderItem,
                                             Product,
                                             )
from rest_framework.response import Response
from rest_framework import status

def get_or_set_order(request):
    """
    Checks if the user has an open order and creates a new order if not found.
    Returns the order object.

    Parameters:
    - request (HttpRequest): The HTTP request object containing user information.

    Returns:
    - order (Order): The newly created or existing order associated with the user.
    """
    order_id = request.user.order_id

    if order_id == -1:
        order = Order(user=request.user) # Create new Order
        order.save()
        request.user.order_id = order.id # Attach User -> Oder
        request.user.save()

    else:
        try:
            # Check for existing order
            order = Order.objects.get(id=order_id, ordered=False)
        except Order.DoesNotExist:
              # Create New Order 
              order = Order(user=request.user) # Create new Order
              order.save()
              request.user.order_id = order.id # Attach User -> Oder
              request.user.save()

    return order

def check_delete_request(request ,id):

    """
    The functio check number of scenerios:
    1. if the OrderItem is exists
    2. If the request come from a user who is allwed to delete the OrderItem
    3. Check if the OrderItem is under open Order

    return: Response object with message if one of the condition has occured
    """

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
    
    # check that the Order is open
    if obj.first().order.ordered :
        data = {
            'message': "The Item you want to delete is under close order",
            'alert': "info",
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

def check_update_requst(request, id):
        
        
        # Check if the OrderItem exists
        obj = OrderItem.objects.filter(id=id)
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

def check_add_to_cart_request(kwargs):
        
        # VALIDATION #
        

        try:
            product = Product.objects.get(slug=kwargs['slug'])
        except Exception as e:
            data = {
                'message': 'The product you ask to add to the cart does not exits',
                'alert': 'danger'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if not product.active:
            data = {
                'message': 'The product you ask to add is not available',
                'alert': 'info'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)   

def check_create_paypal_order_request(request):
     
     """
     The function check 3 things:
     1. If the user has an open Order for him
     2. If there is at list one OrderItem inside the Order
     3. If the user has already add Address
     """
     
     qrs = Order.objects.filter(id=request.user.order_id)

     if request.user.order_id == -1 or not qrs.exists():
          data = {
               'message': 'You have no Item in your cart to purchase. Please add products to you cart before paying',
               'alert' : 'info'
            }
          return Response(data, status=status.HTTP_404_NOT_FOUND)
     
     ####

     if not Address.objects.filter(user=request.user).exists():
          data = {
               'message': 'You have to set your address in the system before continue',
               'alert' : 'info'
            }
          return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
          
     
