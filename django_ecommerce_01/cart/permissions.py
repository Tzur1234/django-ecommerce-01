from typing import Any
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics



class DeleteOrderItemPermission(permissions.BasePermission):
    """
    Custom permission to only allow User to delete his own OrderItem
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if the user is the owner of the order item, False otherwise.
        """
        print('Hello')
        return obj.order.user == request.user