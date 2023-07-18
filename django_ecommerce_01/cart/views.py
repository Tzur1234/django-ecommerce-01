from django.shortcuts import render
from django_ecommerce_01.cart.serializers import ProductSerializer, OrderItemSerializer, AddressSerializer
from django_ecommerce_01.cart.models import (Product,
                                            OrderItem,
                                            ColorVariation,
                                            SizeVariation,
                                            Order,
                                            Address,
                                            Payment)
from django_ecommerce_01.cart.permissions import DeleteOrderItemPermission, IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django_ecommerce_01.cart.utilize import (get_or_set_order,
                                              check_delete_request,
                                              check_update_requst,
                                              check_create_paypal_order_request)
from rest_framework import status
from django.views.generic import TemplateView
from django.conf import settings
import requests
import json
from django.shortcuts import reverse
from django.http import JsonResponse
import ast
import datetime


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PAYPAL_CLIENT_ID'] = settings.PAYPAL_CLIENT_ID
        return context


class ProductListAPIView(generics.ListAPIView):
    """
    accepted methods : GET
    return : Json response - list of products
    """
    permission_classes = [permissions.IsAuthenticated]


    serializer_class = ProductSerializer
    queryset = Product.objects.all()



class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Accepted methods: GET request + slug
    Return: a single product instance 
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
    request(body) : quantity (int), size_id (int), color_id (int)
    response : message (string) , alert (string)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        # Product validation
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

        quantity = request.data["quantity"]
        color = ColorVariation.objects.get(id=request.data["color_id"])
        size = SizeVariation.objects.get(id=request.data["size_id"])

        try:
            # Create / Retreive Order
            order = get_or_set_order(request)

            # Search for existing OrderItem
            order_item = order.items.filter(product=product,
                                            color=color,
                                            size=size,
                                            )

            if order_item.exists():
                order_item = order_item.first()
                last_quantity = order_item.quantity
                order_item.quantity = last_quantity + order_item.quantity  # Update OrderItem quantity
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
            data = {
                'message': f"Error: {e}",
                'alert': 'danger'
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            order_id=self.request.user.order_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # Add extra content to the response:
        # Total price (calculated)
        try:
            order_id = request.user.order_id

            if order_id == -1:
                return Response({'message': 'Your Cart is empty', 'alert': 'info'}, status=status.HTTP_501_NOT_IMPLEMENTED)

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
    """
    Accept method : DELETE
    Return: 204 Response if delet was successfuly completed
    Else: Return False
     """
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
        return Response(data, status=status.HTTP_200_OK)


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
                return Response(data, status=status.HTTP_403_FORBIDDEN)
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
        return Response(data, status=status.HTTP_200_OK)


class AddressUpdateRetrieveAPIView(generics.RetrieveUpdateAPIView):
    """
    The view update the user's address.
    GET : check if the user has already Address object.
    if not : Create a new one and attach it to the user.

    PUT: Validates the address data. Than Update it.

    Permissions (IsOwnerOrReadOnly): the user can update only it's own data.
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
                'saved_address_info': serializer.data,
                'message': "Your address info was saved",
                'alert': "success",
            }
            return Response(data, status.HTTP_200_OK)
        else:
            data = {
                'message': serializer.errors,
                'alert': "danger",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def get_access_token():
    # send request to get the accessToken using your clientID and clientSecret
    #  return accessToken
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    data = {
        'grant_type': 'client_credentials',
    }
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_KEY)
    response = requests.post(url, headers=headers, data=data, auth=auth)
    response_json = response.json()
    return response_json['access_token']


def capture_payment_details(orderID):
    """
    Rce
    """
    access_token = get_access_token()
    if settings.DEBUG:
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{orderID}/capture"
    else:
        url = f"https://api-m.paypal.com/v2/checkout/orders/{orderID}/capture"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.post(url, headers=headers)
    data = response.json()
    return data


class CreateOrderAPIView(APIView):
    """
    get request
    send request to paypal-server to create new order
    return paypal-order object back to the client
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        # Validation #

        response_obj = check_create_paypal_order_request(request)
        if response_obj:
            return response_obj

        # create accessToken using your clientID and clientSecret
        access_token = get_access_token()
        order = Order.objects.get(id=request.user.order_id)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        data = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': {
                        'currency_code': 'USD',
                        'value': f'{order.get_total()}'
                    },
                    'shipping': {
                        'address': {
                            'address_line_1': '123 Main St',
                            'address_line_2': 'Apt 4B',
                            'admin_area_2': 'City',
                            'admin_area_1': 'State',
                            'postal_code': '12345',
                            'country_code': 'US'
                        }
                    }
                }
            ],
        }

        response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders',
                                 headers=headers, data=json.dumps(data))
        response_json = response.json()
        return JsonResponse(response_json)


class ConfirmOrderAPIView(APIView):
    """
    Recieve orderID and check:
    1. If Payment was made succesfully -> Update the
    2. If the payment wasn't made successfuly : return error massage

    """


    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_id = request.data.get('orderID')
        # Use the order_id as needed in your logic
        response_data = capture_payment_details(order_id)


        status = response_data.get('status')
        if status == 'COMPLETED':

       
            # Update last Order status
            order = Order.objects.filter(user=request.user).order_by('-start_date').first()
            order.ordered = True
            order.ordered_date = datetime.date.today()
            order.save()
            request.user.order_id = -1 
            request.user.save()


            # Create new payment object:
            payment = Payment.objects.create(
                order=order,
                successful=True,
                raw_response=json.dumps(response_data),
                amount=float(response_data["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"]),
                payment_method='PayPal'
            )

            data = {
                'message' : 'You have successfully made the payment !',
                'alert' : 'success',
            }

            status = 200
        else:
            data = {
                'message' : 'There was a problem with your payment process. Please try again later or choose a different payment method.',
                'alert' : 'success',
            }
            status = 404



        
        response_data['data'] = data

        # Return your response
        return Response(response_data, status=status)
        

