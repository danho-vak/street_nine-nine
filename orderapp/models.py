from django.db import models

from accountapp.models import User
from addressapp.models import UserAddress

from productapp.models import Product, ProductOption


#  결제할 주문 정보를 담을 model
class Order(models.Model):
    merchant_uid = models.CharField(max_length=100, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='order_user')
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, related_name='order_address', null=True)
    amount = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{}'s order amount : {}".format(self.user.username, self.amount)


#  주문 상품 정보를 담을 model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name='order_product_option')
    quantity = models.IntegerField(default=0)

    # 상품 가격 * 수량
    def sub_total(self):
        return self.product.product_sale_price * self.quantity

    def __str__(self):
        return "{}".format(self.product.product_title)