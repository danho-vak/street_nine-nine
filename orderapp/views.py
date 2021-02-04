from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from iamport import Iamport

from addressapp.models import UserAddress
from cartapp.models import Cart
from orderapp.decorator import order_ownership
from orderapp.models import Order, OrderItem, OrderTransaction

#  User 권한 데코레이터
USER_HAS_ORDER_OWNERSHIP = [order_ownership, login_required]

#  iamport 전역 변수
IAMPORT = Iamport(imp_key=settings.IAMPORT_KEY, imp_secret=settings.IAMPORT_SECRET)

#  주문서를 출력할 view
method_decorator(login_required, 'get')
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

                # 정상적으로 저장되었다면 해당 주문의 merchant_uid와 amount를 리턴
                return JsonResponse({'merchant_uid': merchant_uid, 'amount': order.amount}, status=200)
            except Exception as e:
                print('주문 생성 실패')
                print(e)
                return JsonResponse({}, status=500)
        else:
            print('장바구니 조회 실패')
            return JsonResponse({}, status=500)


#  iamport에 결제가 되었는지 확인한 후 결과를 저장함
#    - ajax로 호출됨(paymentCheck())
@login_required
def orderPaymentCheck(request):
    if request.method == 'POST':

        merchant_uid = request.POST.get('merchant_uid', None)

        try:
            order = Order.objects.get(merchant_uid=merchant_uid)

            response = IAMPORT.find(merchant_uid=merchant_uid)  # iamport에서 merchant_uid로 결제 정보를 찾음
            is_paid = IAMPORT.is_paid(order.amount, response=response)  # return : boolean

            #  iamport에 결제됬다면 DB에 해당 내용 저장
            if is_paid:
                new_order_transaction = OrderTransaction(
                    order=order,
                    imp_uid=response['imp_uid'],
                    merchant_uid=response['merchant_uid'],
                    name=response['name'],
                    amount=response['amount'],
                    paid_at=response['paid_at'],
                    status=response['status'],
                    cancel_amount=response['cancel_amount'],
                    cancel_history=response['cancel_history'],
                    cancel_reason=response['cancel_reason'],
                    cancelled_at=response['cancelled_at'],
                    fail_reason=response['fail_reason'],
                    failed_at=response['failed_at']
                )
                new_order_transaction.save()

                #  장바구니안의 모든 상품 삭제(장바구니 비우기)
                Cart.objects.get(user=request.user).cart_item.all().delete()

                return JsonResponse({'order_id': order.pk}, status=200)

        except ObjectDoesNotExist:
            print('DB 주문 정보 찾을 수 없음')
            return JsonResponse({}, status=500)

#  결제과정에서 취소된 경우 해당 주문 model 삭제
@login_required
def orderPaymentError(request):
    if request.method == 'POST':
        try:
            order = Order.objects.get(user=request.user, merchant_uid=request.POST.get('merchant_uid', None))
            order.delete()
            return JsonResponse({}, status=200)

        except ObjectDoesNotExist:
            print('DB 주문 정보 찾을 수 없음')
            return JsonResponse({}, status=500)


#  User의 주문 내역 List View
@method_decorator(login_required, 'get')
class UserOrderListView(ListView):
    context_object_name = 'order_list'
    template_name = 'orderapp/list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


#  결제 취소 view
def orderPaymentCancel(request):
    if request.method == 'POST':
        order_pk = request.POST.get('order_id', None)
        try:
            order = Order.objects.get(pk=order_pk)  # 주문 정보를 찾고
            try:
                imp_uid = order.order_transaction.imp_uid  # 찾은 주문 정보에서 order_transaction의 imp_uid를 가져옴
                order_transaction = OrderTransaction.objects.filter(order=order, imp_uid=imp_uid)  # 위의 정보로 transaction 찾음
                try:
                    # iamport에 결제 취소 요청
                    cancel_response = IAMPORT.cancel('구매자 요청으로 취소', imp_uid=imp_uid)
                    # 응답 받은 취소 요청 결과를 order_transaction에 반영
                    order_transaction.update(
                        paid_at=cancel_response['paid_at'],
                        status=cancel_response['status'],
                        cancel_amount=cancel_response['cancel_amount'],
                        cancel_history=cancel_response['cancel_history'],
                        cancel_reason=cancel_response['cancel_reason'],
                        cancelled_at=cancel_response['cancelled_at'],
                        fail_reason=cancel_response['fail_reason'],
                        failed_at=cancel_response['failed_at']
                    )
                    return JsonResponse({}, status=200)

                except Iamport.ResponseError as e:  # 취소시 오류 예외처리(이미 취소된 결제는 에러가 발생함)
                    print(e.code)
                    print(e.message)  # 에러난 이유를 알 수 있음
                    return JsonResponse({}, status=500)
                except Iamport.HttpError as http_error:
                    print(http_error.code)
                    print(http_error.reason)  # HTTP not 200 에러난 이유를 알 수 있음
                    return JsonResponse({}, status=500)

            except ObjectDoesNotExist:
                print('DB 주문 트랜잭션 찾을 수 없음')
                return JsonResponse({}, status=500)

        except ObjectDoesNotExist:
            print('DB 주문 정보 찾을 수 없음')
            return JsonResponse({}, status=500)


@method_decorator(USER_HAS_ORDER_OWNERSHIP, 'get')
class OrderDetailView(DetailView):
    model = Order
    context_object_name = 'target_order'
    template_name = 'orderapp/detail.html'
