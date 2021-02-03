from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from iamport import Iamport

from accountapp.models import User
from addressapp.models import UserAddress

from productapp.models import Product, ProductOption


#  결제할 주문 정보를 담을 model
class Order(models.Model):
    merchant_uid = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
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


#  주문한 상품의 결제 상태를 저장할 model
#    - Order 모델에서 가져오는게 아닌, iamport에서 가져온 결제 상태를 담음
class OrderTransaction(models.Model):
    order = models.OneToOneField(Order, related_name='order_transaction', on_delete=models.CASCADE)
    imp_uid = models.CharField(max_length=100, null=False, blank=False)
    merchant_uid = models.CharField(max_length=100, null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    paid_at = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=False, blank=False)
    cancel_amount = models.IntegerField(null=True, blank=True)
    cancel_history = models.CharField(max_length=100, null=True, blank=True)
    cancel_reason = models.CharField(max_length=100, null=True, blank=True)
    cancelled_at = models.CharField(max_length=100, null=True, blank=True)
    fail_reason = models.CharField(max_length=100, null=True, blank=True)
    failed_at = models.CharField(max_length=100, null=True, blank=True)


IAMPORT = Iamport(imp_key=settings.IAMPORT_KEY, imp_secret=settings.IAMPORT_SECRET)

def paymentPrepare(sender, instance, created, *args, **kwargs):
    try:
        response = IAMPORT.prepare(merchant_uid=instance.merchant_uid, amount=instance.amount)
        print('결제 사전정보 등록 결과 : {}'.format(response))
    except Iamport.ResponseError as e:
        print('비정상적인 결제 정보')
    except Iamport.HttpError as http_error:
        print('결제 사전 정보 찾을 수 없음')

def paymentPrepareValidation(sender, instance, created, *args, **kwargs):
    try:
        result = IAMPORT.prepare_validate(merchant_uid=instance.merchant_uid, amount=instance.amount)

        if result is not True:
            pass  # 결제 유효성 실패시 로직


        print('결제 사전정보 유효성 검사 결과 : {}'.format(result))
    except Iamport.ResponseError as e:
        print('비정상적인 결제 정보')
    except Iamport.HttpError as http_error:
        print('결제 사전 정보 찾을 수 없음')


post_save.connect(paymentPrepare, sender=Order)  # Order가 저장되면 paymentPrepare()실행
post_save.connect(paymentPrepareValidation, sender=OrderTransaction)  # OrderTransaction이 저장되면 paymentPrepare()실행
