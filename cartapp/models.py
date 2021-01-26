from django.db import models

from accountapp.models import User
from productapp.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def price_total(self):
        return self.product.product_sale_price * self.quantity

    def __str__(self):
        return "{}'s cart".format(self.user.username)