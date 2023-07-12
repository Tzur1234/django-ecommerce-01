# snippets/views.py
from rest_framework import generics, permissions
from .models import Snippet
from django_ecommerce_01.snippets.serializers import SnippetSerializer
from django_ecommerce_01.snippets.permissions import IsOwnerOrReadOnly



class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    
    def perform_create(self, serializer):  
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        )