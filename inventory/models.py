from django.db import models
from accounts.models import (
    User, Administrator, Customer,
    TrackingModel)
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator)


class Category(TrackingModel):
    category = models.CharField(_("category"), max_length=67,
                                unique=True)
    
    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(TrackingModel):
    product_name = models.CharField(_("product name"), max_length=156)
    unit_price = models.FloatField(_("unit price"), default=0.00)
    stock = models.IntegerField(_("stock"), default=0)
    description = models.TextField(_("description"),
                                    blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                blank=True, null=True)
    image = models.ImageField(
        _("image"), upload_to="products/", default="prod1.png")
    
    def __str__(self):
        return self.product_name


class Rating(TrackingModel):
    product = models.ForeignKey(Product, related_name="products",
                                on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), default=0,
                                validators=[MaxLengthValidator(5),
                                            MinLengthValidator(0)])
    review = models.TextField(_("review"), blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.user.username}-{self.product.product}"
