from django.contrib import admin
from orders.models import OrderItem, Order

admin.site.register(OrderItem)
admin.site.register(Order)
