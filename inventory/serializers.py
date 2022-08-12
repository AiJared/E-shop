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


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True, required=False)

    class Meta:
        model = Product
        fields = ("id", "product_name", "unit_price",
                    "stock", "description", "category",
                    "image", "created_at", "updated_at")

        read_only_fields = ("id",)

    # def update(self, instance, validated_data):
    #     print("update::::")
    #     if validated_data.get('category'):
    #         category_data = validated_data.get('category')
    #         category_serializer = CategorySerializer(data=category_data)

    #         if category_serializer.is_valid():
    #             print("Validity::::", category_serializer.validated_data)
    #             category = category_serializer.update(instance=instance.category,
    #                                                   validated_data=category_serializer.validated_data)
    #             validated_data['category'] = category

    #     return super().update(instance, validated_data)

    
class RatingSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ("id", "product", "rating",
                    "review", "customer", "created_at",
                    "updated_at",)
        read_only_fields = ("id",)
