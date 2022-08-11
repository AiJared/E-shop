from inventory.models import Category, Product, Rating
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "category", "created_at",
                    "updated_at"
                    )
        extra_kwargs = {
            'category': {'validators': []},
        }
        read_only_fields = ("id",)


