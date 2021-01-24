from django.db import models

from accountapp.models import User
from productapp.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
