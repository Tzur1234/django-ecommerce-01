from typing import Any
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        
        # Allow the 'safe mthods' (GET , HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #  return True if the user is the owner of the snippet
        return request.user == obj.owner