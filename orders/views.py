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

