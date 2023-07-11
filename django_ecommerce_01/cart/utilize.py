from django_ecommerce_01.cart.models import Order

"""
The funcion check if the user has associated open Order
if not -
1. create a new Order
2. Keep the Order id in the the session
2. Associate order to the user
"""
def get_or_set_order(request):
    order_id = request.user.order_id


    if order_id == -1:
        order = Order(user=request.user) # Create new Order
        order.save()
        request.user.order_id = order.id # Attach User -> Oder
        request.user.save()

    else:
        try:
            order = Order.objects.get(id=order_id, ordered=False)
            print('Last order was not ordered !')
        except Order.DoesNotExist:
              print('new order is opended')
            # the last Order is closed
              order = Order(user=request.user) # Create new Order
              order.save()
              request.user.order_id = order.id # Attach User -> Oder
              request.user.save()


    return order


# def get_or_set_order(request):
#     order_id = request.session.get('order_id', None)

#     print('request.session["order_id"]: ', request.session['order_id'])

#     print('request.session.session_key', request.session.session_key)

#     print('request.user: ', request.user)

#     if order_id is None:
#         order = Order()
#         order.save()
#         request.session['order_id'] = order.id

#     else:
#         try:
#             order = Order.objects.get(id=order_id, ordered=False)
#         except Order.DoesNotExist:
#             # the last Order is closed
#             order = Order()
#             order.save()
#             request.session['order_id'] = order.id

#     # Associate the Order with user
#     if request.user.is_authenticated and order.user is None:
#         order.user = request.user       
#         order.save()
#     else:
#         print('order.user: ', order.user)
#     return order