from django.db import models

from accountapp.models import User
from productapp.models import Product, ProductOption


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart_user')

    def __str__(self):
        return "{}'s cart".format(self.user.username)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name='cart_product_option')
    quantity = models.IntegerField(default=0)

    def sub_total(self):
        return self.product.product_sale_price * self.quantity

    def __str__(self):
        return "{}  -->  {}'s cart ".format(self.product.product_title, self.cart.user.username)