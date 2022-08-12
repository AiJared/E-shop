from django.db import models
from accounts.models import Customer, TrackingModel
from inventory.models import Product
from django.utils.translation import gettext as _


class OrderItem(TrackingModel):
    item = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(_("quantity"), default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.FloatField(_("total unit price"), default=0.00)

    def __str__(self):
        return self.item.product_name
    

class Order(TrackingModel):
    items = models.ManyToManyField(OrderItem,
                                    related_name="products")
    total = models.FloatField(_("total amount"), default=0.00)
    customer = models.ForeignKey(Customer, 
                                on_delete=models.CASCADE)
    
    def __str__(self):
        return self.customer.user.username
        