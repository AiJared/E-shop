from inventory.serializers import ProductSerializer
from orders.models import Order, OrderItem
from rest_framework.serializers import ModelSerializer


class OrderItemSerializer(ModelSerializer):
    item = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "item", "quantity",
                    "customer", "total", "created_at",
                    "updated_at")
        
        read_only_fields = ("id",)


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "items", "total", "customer",
                    "created_at", "updated_at")

        read_only_fields = ("id",)
        