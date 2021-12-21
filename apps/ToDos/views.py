from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ToDos.models import ToDo
from rest_framework import permissions, filters
from ToDos.serializers import ToDoSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ToDos.pagination import CustomPageNumberPagination


# Create your views here.
# class CreateToDoAPIView(CreateAPIView):
#     serializer_class = ToDoSerializer
#     permission_classes = (IsAuthenticated,)

#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)


# class ToDoListAPIView(ListAPIView):
#     serializer_class = ToDoSerializer
#     permission_classes = (IsAuthenticated,)
#     # queryset = ToDo.objects.all()

#     def get_queryset(self):
#         return ToDo.objects.filter(owner=self.request.user)


class ToDosAPIView(ListCreateAPIView):
    serializer_class = ToDoSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["id", "title", "is_complete"]
    search_fields = ["id", "title", "is_complete"]
    ordering_fields = ["id", "title", "is_complete"]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return ToDo.objects.filter(owner=self.request.user)


# view, edit, delete and update specific ToDo
class ToDoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field ="id"

    def get_queryset(self):
        return ToDo.objects.filter(owner=self.request.user)