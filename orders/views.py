from functools import partial
from django.shortcuts import render, get_object_or_404
from accounts.models import Customer
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdministrator, IsCustomer
from django.db.models import Q


class OrderAPIVIew(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]
    http_method_names = ('get', 'put', 'post', 'patch', 'delete')

    def get_queryset(self):
        user = self.request.user
        customerQs = Customer.objects.get(user=user)
        orderQs = Order.objects.filter(
            Q(customer=customerQs)
        )
        return orderQs
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customerQs = Customer.objects.get(user=request.user)
        serializer.save(customer=customerQs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(
            queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, pk=pk)
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
        