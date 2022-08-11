from django.contrib import admin
from inventory.models import Category, Product, Rating


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Rating)
