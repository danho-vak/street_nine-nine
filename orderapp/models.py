from django.db import models

from accountapp.models import User
from addressapp.models import UserAddress
from cartapp.models import Cart
from productapp.models import Product


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='order_user')
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, related_name='order_address', null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_cart')
    total_price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def delivery_charge(self):
        if self.cart.total_price() >= 50000:
            return 0
        else:
            return 2500

    def __str__(self):
        return "{}'s order > total price : {}".format(self.user.username, self.cart.total_price())