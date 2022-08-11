from django.test import TestCase, Client
from accounts.models import User, Customer
from inventory.models import (Category, 
                                Product, Rating)
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse


class ProductTestCase(APITestCase):
    def setup(self):
        self.client = Client()
        
        self.category = Category.objects.create(
            category="Beverages"
        )
    
    def create_soda(self):
        return Product.objects.create(
            product_name="Sprite",
            unit_price=70.0,
            stock=5,
            description="Sprite 500ml",
            category=self.category,
            image="products.prod1.png",
        )