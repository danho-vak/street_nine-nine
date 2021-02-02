from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from iamport import Iamport

from addressapp.models import UserAddress
from cartapp.models import Cart
from orderapp.decorator import order_ownership
from orderapp.models import Order, OrderItem

USER_HAS_ORDER_OWNERSHIP = [order_ownership, login_required]


method_decorator(USER_HAS_ORDER_OWNERSHIP, 'get')
class OrderListView(ListView):
    model = Cart
    context_object_name = 'target_order'
    template_name = 'orderapp/create.html'

    def get_queryset(self):
        return Cart.objects.get(user=self.request.user)


#  iamport로 결제 요청을 보내기전에 DB에 해당 상품들(장바구니에 담겨있는)을 Order, OrderItem으로 새로 생성
#   - ajax로 호출됨(createOrder())
@login_required
def orderCreateView(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        if cart:
            merchant_uid = 'merchant_' + timezone.localtime().strftime('%Y%m%d%H%M%S%f')  # 고유한 주문번호 생성(시간으로 밀리세컨까지)

            # 새로운 주문 생성
            try:
                address = UserAddress.objects.get(pk=request.POST.get('address_pk', None))
                new_order = Order(
                    merchant_uid=merchant_uid,
                    user=cart.user,
                    address=address,
                    amount=cart.total_price()
                )
                new_order.save()

                #  생성된 주문 object의 pk로 주문 상품 object를 생성(장바구니 item > 주문 item)
                order = Order.objects.get(merchant_uid=merchant_uid)
                for item in cart.cart_item.all():
                    new_order_item = OrderItem(
                        order=order,
                        product=item.product,
                        product_option=item.product_option,
                        quantity=item.quantity
                    )
                    new_order_item.save()

                # 정상적으로 저장되었다면 해당 주문의 merchant_uid를 리턴
                return JsonResponse({'merchant_uid': merchant_uid, 'amount': order.amount}, status=200)
            except Exception as e:
                print('주문 생성 실패')
                print(e)
                return JsonResponse({}, status=500)
        else:
            print('장바구니 조회 실패')
            return JsonResponse({}, status=500)


def orderPaymentCheck(request):
    if request.method == 'POST':
        iamport = Iamport(imp_key=settings.IAMPORT_KEY, imp_secret=settings.IAMPORT_SECRET)
        merchant_uid = request.POST.get('merchant_uid', None)

        try:
            order = Order.objects.get(merchant_uid=merchant_uid)

            response = iamport.find(merchant_uid=merchant_uid)  # iamport에서 merchant_uid로 결제 정보를 찾음
            # iamport에서 위의 find()를 통해 응답 받은 response를 가지고 실제 결제된 금액이 맞는지 확인
            print(response)
            is_paid = iamport.is_paid(order.amount, response=response)

            print(is_paid)

        except ObjectDoesNotExist:
            print('DB 주문 정보 찾을 수 없음')
            return JsonResponse({}, status=500)

