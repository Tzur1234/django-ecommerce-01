from typing import Any
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import generics


# Permission for Address-Update-Retrieve-APIView
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET, HEAD, and OPTIONS requests to all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow PUT requests only if the user is the owner of the Address instance
        return view.get_object().user == request.user

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