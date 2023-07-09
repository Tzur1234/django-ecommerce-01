from django.shortcuts import render
from rest_framework import generics , viewsets

from django_ecommerce_01.todos.serializers import TodoSerializer
from django_ecommerce_01.todos.models import Todo


# class TodoListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer

# class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer