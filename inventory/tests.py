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

    def test_list_products(self):
        response = self.client.get(api_reverse("api:products"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        sprite = self.create_soda()
        expected = [
            {
                "id": sprite.id,
                'product_name': 'sprite',
                'unit_price': 70.00,
                'stock': 5,
                'description': 'Sprite 500ml',
                # 'category':
                'image': 'products/prod1.png'
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_create_product(self):
        self.assertEqual(Product.objects.count(), 0)
        body = {
            'product_name': 'Sprite',
            'unit_price': 70.0,
            'stock': 5,
            'description': 'Sprite 500ml',
            'category': 1,
            'image': 'products/prod1.png',
        }
        response = self.client.post(api_reverse(
            "api:products"), body, 'application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.get()

        expected = {
            'id': product.id,
            'product_name': 'Sprite',
            'unit_price': 70.0,
            'stock': 5,
            'description': 'Sprite 500ml',
            'category': 1,
            'image': 'products/prod1.png'
        }
        self.assertEqual(response.json(), expected)
    
    def test_get_product(self):
        sprite = self.create_soda()
        expected = {
            'id': sprite.id,
            'product_name': 'Sprite',
            'unit_price': 70.0,
            'stock': 5,
            'description': 'Sprite 500ml',
            'category': 1,
            'image': 'products/prod1.png',
        }
        response = self.client.get(api_reverse(
            'api:products', kwargs={"pk": sprite.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
    
    def test_get_product_after_edition(self):
        sprite = self.create_soda()
        expected = {
            'id': sprite.id,
            'product_name': 'Sprite',
            'unit_price': 70.0,
            'stock': 5,
            'description': 'Sprite 500ml',
            'category': 1,
            'image': 'products/prod1.png',
        }
        response = self.client.get(api_reverse(
            'api:products', kwargs={'pk': sprite.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

        sprite.product_name = "Coca-Cola"
        sprite.description = 'Coca-Cola 500ml'
        sprite.save()

        expected = {
            'id': sprite.id,
            'product_name': 'Coca-Cola',
            'unit_price': 70.00,
            'stock': 5,
            'description': 'Coca-Cola 500ml',
            'category': 1,
            'image': 'products/prod1.png',
        }
        response = self.client.get(api_reverse(
            'api:products', kwargs={'pk': sprite.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_update_product(self):
        sprite = self.create_soda()
        response = self.client.get(api_reverse(
            'api:products', kwargs={'pk': sprite.id}))
        self.assertEqual(response.status_code, 200)

        # Test HTTP PUT
        body = {
            'id': sprite.id,
            'product_name': 'Coca-Cola',
            'unit_price': 70.0,
            'stock': 10,
            'description': 'Coca-Cola 500ml',
            'category': 1,
            'image': 'products/prod1.png',
        }

        expected = {
            'id': sprite.id,
            'product_name': 'Coca-Cola',
            'unit_price': 70.0,
            'stock': 10,
            'description': 'Coca-Cola 500ml',
            'category': 1,
            'image': 'products/prod1.png',
        }
        response = self.client.put(api_reverse(
            'api:products', kwargs={'pk': sprite.id}),
            body, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

        # Test HTTP PATCH
        body = {
            'unit_price': 100.0,
            'stock': 7
        }
        expected = {
            'id': sprite.id,
            'product_name': 'Coca-Cola',
            'unit_price': 100.0,
            'stock': 7,
            'description': 'Coca-Cola 500ml',
            'category': 1,
            'image': 'products/prod1.png'
        }
        response = self.client.patch(api_reverse(
            'api:products', kwargs={'pk': sprite.id}),
            body, 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_delete_product(self):
        sprite = self.create_soda()
        response = self.client.delete(api_reverse(
            'api:products', kwargs={'pk': sprite.id}))
        self.assertEqual(response.status_code, 405)


class CategoryTestCase(TestCase):
    def setup(self):
        self.client = Client()

    def create_beverage(self):
        return Category.objects.create(
            category="Beverages"
        )


class RatingTestCase(TestCase):
    def setup(self):
        self.client = Client()
        self.category = Category.objects.create(
            category="Beverages"
        )
        self.user = User.objects.create(
            username = "testuser",
            full_name="test user",
            email="testuser@gmail.com",
            phone="+254712345678",
            role="Customer",
            is_active=True,
            is_admin=False,
            is_staff=False
        )
        self.customer = Customer.objects.create(
            user=self.user,
            bio="fly high",
            profile_picture="profile/defualt.png",
            city = "sun city",
            address = "151",
            postal_code="20116",
            town="river town",
            estate="villa estate"  
        )
        self.coke = Product.objects.create(
            product_name="Coca-Cola",
            unit_price=80,
            stock=10,
            description="Coca-Cola 500ml",
            category=self.category,
            image="products/coke.png"
        )

    def create_rating(self):
        return Rating.objects.create(
            product=self.coke,
            rating=4,
            review="was not cold",
            customer=self.customer
        )